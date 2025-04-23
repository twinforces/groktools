# grokpatcher.py
# Collects diffs from .grokpatch files and generates a doit.sh script for manual patching.
# Follows docs/grokpatcher.md, docs/prompts/diffu_prompt.md, and docs/prompts/bestpractices.md.

import sys
import logging
import os
from pathlib import Path

# Constants
LOG_FILE = "grokpatcher.log"
MAX_PATCH_SIZE = 1024 * 1024  # 1MB limit for patch files

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GrokPatcher:
    def __init__(self):
        self.version_count = 0
        self.current_file = None
        self.input_path = None
        self.output_path = None
        self.diffextract_script = "src/diffextract.py"
        self.diffs = []  # List to store (input_path, output_path, diff_file) tuples
        self.diff_files = []  # List to keep track of generated diff files

    def validate_metadata(self, input_path, output_path):
        """Validate input and output paths."""
        logging.debug(f"Validating metadata: input_path={input_path}, output_path={output_path}")
        if not Path(input_path).exists():
            logging.error(f"Input file does not exist: {input_path}")
            raise ValueError(f"Input file does not exist: {input_path}")
        if not output_path:
            logging.error("Output path not specified")
            raise ValueError("Output path not specified")

    def extract_diff(self, diff_content):
        """Extract the diff from the content and save it to a file."""
        logging.debug("Extracting diff content")
        # Write diff to temp file for diffextract.py
        with open("temp.grokpatch", "w", encoding="utf-8") as f:
            f.write(diff_content)
        
        # Extract the diff using diffextract.py into another temp file
        diff_file = f"diff{len(self.diff_files) + 1}.diff"
        cmd_extract = f"python3 {self.diffextract_script} temp.grokpatch > {diff_file}"
        logging.debug(f"Executing: {cmd_extract}")
        result = os.system(cmd_extract)
        if result != 0:
            logging.error(f"Error extracting diff: {result}")
            raise RuntimeError(f"Error extracting diff: {result}")

        # Log the content of the diff file for debugging
        with open(diff_file, "r", encoding="utf-8") as f:
            diff_content = f.read()
        logging.debug(f"Extracted diff content ({diff_file}):\n{diff_content}")

        self.diff_files.append(diff_file)
        return diff_file

    def process_patch(self):
        """Process a .grokpatch file from stdin, collecting diffs and generating doit.sh."""
        logging.debug("Starting process_patch")
        # Read patch content from stdin incrementally
        patch_content = ""
        while True:
            chunk = sys.stdin.read(1024)
            if not chunk:
                break
            patch_content += chunk
            logging.debug(f"Read chunk of {len(chunk)} bytes")
        if not patch_content:
            logging.error("No input received from stdin")
            print("Error: No input received from stdin", file=sys.stderr)
            sys.exit(1)
        logging.debug(f"Read patch content:\n{patch_content}")
        
        # Parse metadata
        lines = patch_content.splitlines()
        logging.debug(f"Split into {len(lines)} lines")
        diff_lines = []
        in_diff = False
        current_input_path = None
        current_output_path = None
        current_version_count = 0
        current_file = None
        
        for line in lines:
            logging.debug(f"Processing line: '{line}' (in_diff={in_diff}, diff_lines length={len(diff_lines)})")
            if line.startswith("!INPUT:"):
                current_input_path = line[len("!INPUT:"):].strip()
                logging.debug(f"Set current_input_path: {current_input_path}")
            elif line.startswith("!OUTPUT:"):
                current_output_path = line[len("!OUTPUT:"):].strip()
                # Reset version count if we're patching a new file
                if current_file != current_output_path:
                    current_file = current_output_path
                    current_version_count = 0
                logging.debug(f"Set current_output_path: {current_output_path}, current_version_count: {current_version_count}")
            elif line.strip() == "!GO!":
                logging.debug("Encountered !GO!")
                if not current_input_path or not current_output_path:
                    logging.error("!GO! encountered without INPUT or OUTPUT set")
                    print("Error: !GO! encountered without INPUT or OUTPUT set", file=sys.stderr)
                    sys.exit(1)
                # Extracted diff content (excluding metadata)
                diff_content = "\n".join(diff_lines) + "\n\n"
                logging.debug(f"Diff content to extract:\n{diff_content}")
                # Extract the diff and store it
                diff_file = self.extract_diff(diff_content)
                version_suffix = f".{current_version_count}"
                versioned_output = f"{current_output_path}{version_suffix}"
                self.validate_metadata(current_input_path, current_output_path)
                self.diffs.append((current_input_path, versioned_output, diff_file))
                # Increment version count after collecting a diff
                current_version_count += 1
                logging.debug(f"Added diff: input_path={current_input_path}, output_path={versioned_output}, diff_file={diff_file}")
                diff_lines = []  # Reset diff lines for the next patch
                in_diff = False
            elif line.strip() == "!NEXT!":
                current_version_count += 1
                logging.debug(f"Encountered !NEXT!, current_version_count: {current_version_count}")
            elif line.strip() == "!DONE!":
                logging.debug("Encountered !DONE!")
                # Process any remaining diff content before generating doit.sh
                if in_diff and diff_lines:
                    if not current_input_path or not current_output_path:
                        logging.error("!DONE! encountered with pending diff but without INPUT or OUTPUT set")
                        print("Error: !DONE! encountered with pending diff but without INPUT or OUTPUT set", file=sys.stderr)
                        sys.exit(1)
                    diff_content = "\n".join(diff_lines) + "\n\n"
                    logging.debug(f"Processing final diff content:\n{diff_content}")
                    diff_file = self.extract_diff(diff_content)
                    version_suffix = f".{current_version_count}"
                    versioned_output = f"{current_output_path}{version_suffix}"
                    self.validate_metadata(current_input_path, current_output_path)
                    self.diffs.append((current_input_path, versioned_output, diff_file))
                    current_version_count += 1
                    logging.debug(f"Added final diff: input_path={current_input_path}, output_path={versioned_output}, diff_file={diff_file}")
                # Generate doit.sh with all patch commands
                with open("doit.sh", "w") as f:
                    f.write("#!/bin/bash\n")
                    f.write("# Generated by grokpatcher.py to apply patches manually\n")
                    f.write("set -e\n")
                    if not self.diffs:
                        logging.error("No diffs collected to apply")
                        print("Error: No diffs collected to apply", file=sys.stderr)
                        sys.exit(1)
                    for input_path, output_path, diff_file in self.diffs:
                        # Run gpatch and check the exit code explicitly
                        cmd = f"gpatch -p0 --verbose --output={output_path} {input_path} < {diff_file}"
                        f.write(f"echo 'Applying patch: {cmd}'\n")
                        f.write(f"{cmd} || {{ echo 'Error: Failed to apply patch {diff_file}'; exit 1; }}\n")
                        f.write(f"if [ ! -s {output_path} ]; then\n")
                        f.write(f"    echo 'Error: Output file {output_path} is empty or does not exist'\n")
                        f.write(f"    exit 1\n")
                        f.write(f"fi\n")
                    # Replace the original file with the latest version
                    if current_output_path and current_version_count > 0:
                        latest_version = f"{current_output_path}.{current_version_count - 1}"
                        if os.path.exists(latest_version):
                            f.write(f"mv {latest_version} {current_output_path}\n")
                            f.write(f"echo 'Patch set completed: {current_output_path} updated'\n")
                        else:
                            f.write("echo 'Patch set completed'\n")
                    else:
                        f.write("echo 'Patch set completed'\n")
                # Make doit.sh executable
                os.chmod("doit.sh", 0o755)
                print("Generated doit.sh with patch commands. Run './doit.sh' to apply patches.")
                logging.debug("Generated doit.sh")
                break
            elif line.strip().startswith("---"):
                in_diff = True
                diff_lines.append(line)
                logging.debug("Started diff section")
            elif in_diff:
                diff_lines.append(line)
                logging.debug(f"Added line to diff_lines: {line}")
        else:
            logging.error("Reached end of input without encountering !DONE!")
            print("Error: !DONE! marker not found in input", file=sys.stderr)
            sys.exit(1)

def main():
    grok_patcher = GrokPatcher()
    grok_patcher.process_patch()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        print("Interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)
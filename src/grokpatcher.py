# grokpatcher.py
# Applies .grokpatch files using gpatch, supporting versioning and multi-file patches.
# Follows docs/grokpatcher.md, docs/prompts/diffu_prompt.md, and docs/prompts/bestpractices.md.

import sys
import logging
import os
import time
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

    def validate_metadata(self, input_path, output_path):
        """Validate input and output paths."""
        if not Path(input_path).exists():
            logging.error(f"Input file does not exist: {input_path}")
            raise ValueError(f"Input file does not exist: {input_path}")
        if not output_path:
            logging.error("Output path not specified")
            raise ValueError("Output path not specified")

    def apply_patch(self, input_path, output_path, diff_content):
        """Apply a patch to the input file, creating a versioned output file."""
        self.validate_metadata(input_path, output_path)
        
        # Write diff to temp file for gpatch, ensuring UTF-8 encoding
        with open("temp.grokpatch", "w", encoding="utf-8") as f:
            f.write(diff_content)
        # Ensure the temp file is flushed to disk
        with open("temp.grokpatch", "r") as f:
            os.fsync(f.fileno())
        
        # Extract the diff using diffextract.py into another temp file
        extracted_diff_file = "temp_extracted_diff.diff"
        cmd_extract = f"python3 {self.diffextract_script} temp.grokpatch > {extracted_diff_file}"
        logging.debug(f"Executing: {cmd_extract}")
        result = os.system(cmd_extract)
        if result != 0:
            logging.error(f"Error extracting diff: {result}")
            raise RuntimeError(f"Error extracting diff: {result}")

        # Ensure the extracted diff file is flushed to disk
        with open(extracted_diff_file, "r") as f:
            os.fsync(f.fileno())

        # Log the content of extracted_diff_file for debugging
        with open(extracted_diff_file, "r", encoding="utf-8") as f:
            diff_content = f.read()
        logging.debug(f"Extracted diff content:\n{diff_content}")

        version_suffix = f".{self.version_count}"
        versioned_output = f"{output_path}{version_suffix}"
        # Apply the patch using gpatch with -p0 and --verbose, using os.system to match manual test
        cmd = f"gpatch -p0 --verbose --output={versioned_output} {input_path} < {extracted_diff_file} 2> gpatch_error.log"
        logging.debug(f"Executing with os.system: {cmd}")
        result = os.system(cmd)
        if result != 0:
            with open("gpatch_error.log", "r", encoding="utf-8") as f:
                error_output = f.read()
            logging.error(f"Error applying patch to {versioned_output}: {result}")
            logging.error(f"gpatch error output: {error_output}")
            raise RuntimeError(f"Error applying patch to {versioned_output}: {result}\ngpatch error output: {error_output}")
        
        # Ensure the output file is flushed to disk
        if os.path.exists(versioned_output):
            with open(versioned_output, "rb") as f:
                os.fsync(f.fileno())
        # Add a longer sleep to allow file system to settle
        time.sleep(0.2)

        # Verify the output file was created and has content
        if not os.path.exists(versioned_output):
            logging.error(f"Output file not created: {versioned_output}")
            raise RuntimeError(f"Output file not created: {versioned_output}")
        if os.path.getsize(versioned_output) == 0:
            logging.error(f"Output file is empty: {versioned_output}")
            raise RuntimeError(f"Output file is empty: {versioned_output}")
        
        # Clean up temp files
        os.remove("temp.grokpatch")
        os.remove(extracted_diff_file)
        if os.path.exists("gpatch_error.log"):
            with open("gpatch_error.log", "r", encoding="utf-8") as f:
                error_output = f.read()
            logging.debug(f"gpatch verbose output: {error_output}")
            os.remove("gpatch_error.log")
        return versioned_output

    def process_patch(self):
        """Process a .grokpatch file from stdin, handling metadata and applying patches."""
        # Read patch content from stdin with UTF-8 encoding
        patch_content = sys.stdin.read()
        
        # Parse metadata
        lines = patch_content.splitlines()
        diff_lines = []
        in_diff = False
        
        for line in lines:
            if line.startswith("!INPUT:"):
                self.input_path = line[len("!INPUT:"):].strip()
            elif line.startswith("!OUTPUT:"):
                self.output_path = line[len("!OUTPUT:"):].strip()
                # Reset version count if we're patching a new file
                if self.current_file != self.output_path:
                    self.current_file = self.output_path
                    self.version_count = 0
            elif line.strip() == "!GO!":
                # Extracted diff content (excluding metadata)
                diff_content = "\n".join(diff_lines) + "\n\n"
                # Apply the patch
                versioned_output = self.apply_patch(self.input_path, self.output_path, diff_content)
                print(f"Patch applied to {versioned_output}")
                # Increment version count after applying a patch
                self.version_count += 1
            elif line.strip() == "!NEXT!":
                self.version_count += 1
            elif line.strip() == "!DONE!":
                # Replace the original file with the latest version
                latest_version = f"{self.output_path}.{self.version_count - 1}"
                if os.path.exists(latest_version):
                    os.rename(latest_version, self.output_path)
                    print(f"Patch set completed: {self.output_path} updated")
                else:
                    print("Patch set completed")
                break
            elif line.startswith("---"):
                in_diff = True
                diff_lines.append(line)
            elif in_diff:
                diff_lines.append(line)

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
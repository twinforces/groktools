# grokpatcher.py
# Applies .grokpatch copypastas to Python scripts, creating versioned files and using diffextract.py and gpatch.
# Follows docs/prompts/grokpatcher_prompt.md and docs/prompts/bestpractices.md.

import subprocess
import sys
import os
import shutil
from pathlib import Path
import logging

# Constants
LOG_FILE = "grokpatcher.log"
MAX_PATCH_SIZE = 1024 * 1024  # 1MB limit for pasted patches
TEMP_FILE = "temp.grokpatch"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_grokpatch(patch_content):
    """Parse .grokpatch content, returning metadata, diff, and markers."""
    lines = patch_content.splitlines()
    metadata = {}
    diff_lines = []
    marker = None

    for line in lines:
        if line.startswith("!INPUT:"):
            metadata["input"] = line[len("!INPUT:"):].strip()
        elif line.startswith("!OUTPUT:"):
            metadata["output"] = line[len("!OUTPUT:"):].strip()
        elif line.strip() in ("!GO!", "!DONE!", "!NEXT!"):
            marker = line.strip()
            break
        else:
            diff_lines.append(line)

    return metadata, "\n".join(diff_lines), marker

def validate_metadata(metadata, current_file):
    """Validate metadata, ensuring input file matches current file."""
    input_path = metadata.get("input")
    output_path = metadata.get("output")
    if not input_path or not output_path:
        logging.error("Missing !INPUT or !OUTPUT in metadata")
        raise ValueError("Missing !INPUT or !OUTPUT in metadata")
    if input_path != current_file:
        logging.error(f"Input file mismatch: expected {current_file}, got {input_path}")
        raise ValueError(f"Input file mismatch: expected {current_file}, got {input_path}")
    if not Path(input_path).exists():
        logging.error(f"Input file does not exist: {input_path}")
        raise ValueError(f"Input file does not exist: {input_path}")

def apply_patch(diff_content, input_file, version_suffix):
    """Apply diff using gpatch, saving to a versioned file."""
    output_file = f"{input_file}.{version_suffix}"
    try:
        # Copy input file to versioned file
        shutil.copy2(input_file, output_file)
        # Apply patch
        result = subprocess.run(
            ["gpatch", "-p1", "-i", "-"],
            input=diff_content,
            text=True,
            capture_output=True,
            check=True
        )
        logging.info(f"Patch applied to {output_file}")
        print(f"Patch applied to {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Error applying patch to {output_file}: {e.stderr}")
        print(f"Error applying patch to {output_file}: {e.stderr}")
        return None

def extract_diff(patch_content):
    """Extract and unescape diff using diffextract.py."""
    try:
        with open(TEMP_FILE, "w") as f:
            f.write(patch_content)
        result = subprocess.run(
            ["python", "src/diffextract.py", TEMP_FILE],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error extracting diff: {e.stderr}")
        print(f"Error extracting diff: {e.stderr}")
        return None
    finally:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

def main():
    """Process .grokpatch copypastas from stdin, applying patches and versioning files."""
    logging.debug("Starting grokpatcher")
    print("Paste .grokpatch content (end with !GO!, !NEXT!, or !DONE!):")
    
    current_file = None
    version_count = 0
    patch_content = ""
    versioned_files = []

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        patch_content += line
        if len(patch_content) > MAX_PATCH_SIZE:
            logging.error("Patch size exceeds limit")
            print("Error: Patch size exceeds limit")
            sys.exit(1)
        if line.strip() in ("!GO!", "!NEXT!", "!DONE!"):
            try:
                metadata, diff, marker = parse_grokpatch(patch_content)

                if marker == "!DONE!":
                    if current_file and versioned_files:
                        # Save final version as original file
                        final_file = versioned_files[-1]
                        shutil.move(final_file, current_file)
                        logging.info(f"Finalized {current_file} from {final_file}")
                        print(f"Finalized {current_file} from {final_file}")
                    logging.info("Patch set completed")
                    print("Patch set completed")
                    break

                if marker == "!NEXT!":
                    if current_file and versioned_files:
                        # Finalize current file
                        final_file = versioned_files[-1]
                        shutil.move(final_file, current_file)
                        logging.info(f"Finalized {current_file} from {final_file}")
                        print(f"Finalized {current_file} from {final_file}")
                    current_file = None
                    version_count = 0
                    versioned_files = []
                    patch_content = ""
                    continue

                if marker == "!GO!":
                    if not current_file:
                        current_file = metadata.get("input")
                    validate_metadata(metadata, current_file)
                    diff_content = extract_diff(patch_content)
                    if not diff_content:
                        sys.exit(1)
                    version_count += 1
                    output_file = apply_patch(diff_content, current_file, version_count)
                    if output_file:
                        versioned_files.append(output_file)
                    else:
                        sys.exit(1)
                    patch_content = ""
                    continue

            except ValueError as e:
                logging.error(f"Validation error: {str(e)}")
                print(f"Error: {str(e)}")
                sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        print("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
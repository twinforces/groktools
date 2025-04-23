# diffextract.py
# Extracts and unescapes unified diffs from .grokpatch files for gpatch.
# Adds real timestamps to diff headers based on the input file's modification time.
# Follows docs/grokpatcher.md, docs/prompts/diffu_prompt.md, and docs/prompts/bestpractices.md.

import sys
import logging
import os
from pathlib import Path
from datetime import datetime

# Constants
LOG_FILE = "diffextract.log"
MAX_PATCH_SIZE = 1024 * 1024  # 1MB limit for patch files

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_file(patch_file):
    """Validate the .grokpatch file exists and is readable."""
    if not Path(patch_file).exists():
        logging.error(f"Patch file does not exist: {patch_file}")
        raise ValueError(f"Patch file does not exist: {patch_file}")
    if Path(patch_file).stat().st_size > MAX_PATCH_SIZE:
        logging.error(f"Patch file size exceeds limit: {patch_file}")
        raise ValueError(f"Patch file size exceeds limit")

def extract_diff(patch_content):
    """Extract unified diff from .grokpatch, unescaping backticks, and update timestamps."""
    lines = patch_content.splitlines()
    diff_lines = []
    in_diff = False
    input_path = None

    # Parse !INPUT: to get the input file path
    for line in lines:
        if line.startswith("!INPUT:"):
            input_path = line[len("!INPUT:"):].strip()
        if line.startswith("---"):
            in_diff = True
        if in_diff:
            # Unescape backticks
            unescaped_line = line.replace("\\`", "`")
            diff_lines.append(unescaped_line)

    if not diff_lines:
        logging.error("No valid diff found in .grokpatch")
        raise ValueError("No valid diff found in .grokpatch")

    if not input_path or not Path(input_path).exists():
        logging.warning(f"Input file not found for timestamp: {input_path}, using dummy timestamp")
        timestamp = "1970-01-01 00:00:00"
    else:
        mtime = os.path.getmtime(input_path)
        timestamp = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    # Update timestamps in diff headers
    updated_diff_lines = []
    for line in diff_lines:
        if line.startswith("---"):
            parts = line.split("\t", 1)
            updated_diff_lines.append(f"{parts[0]}\t{timestamp}")
        elif line.startswith("+++"):
            parts = line.split("\t", 1)
            updated_diff_lines.append(f"{parts[0]}\t{timestamp}")
        else:
            updated_diff_lines.append(line)

    # Ensure trailing newline and blank line after hunk
    return "\n".join(updated_diff_lines) + "\n\n"

def main():
    """Extract and unescape diff from a .grokpatch file, outputting to stdout."""
    if len(sys.argv) != 2:
        logging.error("Usage: python diffextract.py <patch_file>")
        print("Usage: python diffextract.py <patch_file>", file=sys.stderr)
        sys.exit(1)

    patch_file = sys.argv[1]
    logging.debug(f"Starting diffextract: patch_file={patch_file}")

    try:
        validate_file(patch_file)
        with open(patch_file, "r") as f:
            patch_content = f.read()
        diff_content = extract_diff(patch_content)
        print(diff_content, end="")
    except (ValueError, IOError) as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

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
# diffextract.py
# Extracts and unescapes unified diffs from .grokpatch files for gpatch.
# Follows docs/grokpatcher.md, docs/prompts/diffu_prompt.md, and docs/prompts/bestpractices.md.

import sys
import logging
from pathlib import Path

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
    """Extract unified diff from .grokpatch, unescaping backticks."""
    lines = patch_content.splitlines()
    diff_lines = []
    in_diff = False

    for line in lines:
        if line.startswith("!INPUT:") or line.startswith("!OUTPUT:") or line.strip() in ("!GO!", "!NEXT!", "!DONE!"):
            continue
        if line.startswith("---"):
            in_diff = True
        if in_diff:
            # Unescape backticks
            unescaped_line = line.replace("\\`", "`")
            diff_lines.append(unescaped_line)

    if not diff_lines:
        logging.error("No valid diff found in .grokpatch")
        raise ValueError("No valid diff found in .grokpatch")

    return "\n".join(diff_lines) + "\n"

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
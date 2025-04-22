import re
import sys
import os
import difflib
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Optional

# Configure logging to a separate file
logging.basicConfig(
    filename="grokpatcher.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_grokpatcher_patch(patch_content: str) -> List[Tuple[Dict[str, str], List[Dict[str, str]]]]:
    """Parse a GrokPatcher patch into a list of (header, sections) pairs."""
    patches = []
    current_header = {}
    current_section = None
    content_lines = []
    sections = []
    lines = patch_content.splitlines()
    i = 0
    in_content = False

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue
        if line == "!GO!":
            if current_section:
                current_section["Content"] = "\n".join(content_lines).rstrip()
                sections.append(current_section)
                current_section = None
                content_lines = []
                in_content = False
            continue
        if line in ["!NEXT!", "!DONE!"]:
            if current_section:
                current_section["Content"] = "\n".join(content_lines).rstrip()
                sections.append(current_section)
            if current_header and sections:
                patches.append((current_header, sections))
            current_header = {}
            current_section = None
            content_lines = []
            sections = []
            in_content = False
            continue
        if line.startswith("# GrokPatcher v1.0"):
            continue
        if line.startswith("# ") and not in_content:
            parts = line[2:].split(":", 1)
            if len(parts) != 2:
                logging.error(f"Invalid header line: {line}")
                raise ValueError(f"Invalid header line: {line}")
            key, value = parts
            current_header[key.strip()] = value.strip()
        elif line == "[Section]":
            if current_section:
                current_section["Content"] = "\n".join(content_lines).rstrip()
                sections.append(current_section)
            current_section = {}
            content_lines = []
            in_content = False
        elif current_section is not None:
            if line.startswith("Anchor:"):
                current_section["Anchor"] = line.split(":", 1)[1].strip()
            elif line.startswith("AnchorType:"):
                current_section["AnchorType"] = line.split(":", 1)[1].strip()
            elif line.startswith("Action:"):
                current_section["Action"] = line.split(":", 1)[1].strip()
            elif line.startswith("Content:"):
                in_content = True
                continue
            elif in_content:
                content_lines.append(line[4:])  # Remove 4-space indent

    # Handle the last section and patch
    if current_section:
        current_section["Content"] = "\n".join(content_lines).rstrip()
        sections.append(current_section)
    if current_header and sections:
        patches.append((current_header, sections))

    return patches

def apply_patch(input_file: str, patches: List[Dict[str, str]], output_file: str, target_file: str, verbose: bool = False) -> str:
    """Apply patches to the input file and return the updated content."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content

        for patch in patches:
            anchor = patch["Anchor"]
            action = patch["Action"]
            patch_anchor_type = patch.get("AnchorType", "artificial")
            # De-escape backticks
            new_content = patch["Content"].replace("\\`", "`")

            # Construct anchor regex based on type
            if patch_anchor_type == "natural":
                anchor_re = re.compile(rf"^{re.escape(anchor)}$", re.MULTILINE)
            else:
                anchor_re = re.compile(rf"^# ARTIFICIAL ANCHOR: {re.escape(anchor)}$", re.MULTILINE)
            
            match = anchor_re.search(content)
            if not match:
                logging.error(f"{patch_anchor_type.capitalize()} anchor '{anchor}' not found in {input_file}")
                raise ValueError(f"{patch_anchor_type.capitalize()} anchor '{anchor}' not found in {input_file}")
            
            start_pos = match.start()
            next_anchor = re.compile(r"^(# ARTIFICIAL ANCHOR: .+|def\s+\w+\s*\(.*\):|if\s+.*:|\s*for\s+.*:|\s*while\s+.*:|\s*class\s+\w+\s*:)", re.MULTILINE)
            next_match = next_anchor.search(content, match.end())
            end_pos = next_match.start() if next_match else len(content)
            
            if action == "replace":
                if patch_anchor_type == "artificial":
                    content = content[:start_pos] + f"# ARTIFICIAL ANCHOR: {anchor}\n{new_content}\n" + content[end_pos:]
                else:
                    content = content[:start_pos] + f"{new_content}\n" + content[end_pos:]
            elif action == "insert":
                content = content[:match.end()] + f"\n{new_content}\n" + content[match.end():]
            elif action == "delete":
                content = content[:start_pos] + content[end_pos:]
            else:
                logging.error(f"Unknown action '{action}'")
                raise ValueError(f"Unknown action '{action}'")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Patched file written to {output_file}")
        print(f"Patched file written to {output_file}")

        # Log diff if verbose
        if verbose:
            original_lines = original_content.splitlines()
            updated_lines = content.splitlines()
            diff = list(difflib.unified_diff(original_lines, updated_lines, fromfile=input_file, tofile=output_file))
            if diff:
                logging.info("Diff of changes:\n" + "\n".join(diff))
            else:
                logging.info("No changes detected in diff.")

        return content

    except Exception as e:
        logging.error(f"Failed to apply patch: {str(e)}", exc_info=True)
        raise

def build_revert_patch(original_file: str, updated_file: str, revert_output: str) -> None:
    """Builds a revert patch using patchBuilder.py."""
    try:
        from patchBuilder import PatchBuilder
        builder = PatchBuilder(Path(updated_file).name, updated_file, original_file)
        builder.generate_patch()
        builder.build(revert_output)
        logging.info(f"Revert patch generated at {revert_output}")
    except Exception as e:
        logging.error(f"Failed to build revert patch: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to build revert patch: {str(e)}")

def main():
    """Run GrokPatcher as a continuous service with optional verbose and revert modes."""
    import argparse
    parser = argparse.ArgumentParser(description="GrokPatcher applies patches to Python scripts.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode with diff logging.")
    parser.add_argument("--buildRevert", type=str, help="Generate a revert patch and save to the specified path.")
    args = parser.parse_args()

    print("GrokPatcher v1.0 started. Paste patches (end with '!GO!', '!NEXT!', or '!DONE!').")
    
    # Read entire input from stdin until EOF
    patch_content = ""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:  # EOF or Ctrl+D/Ctrl+Z
                break
            patch_content += line
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")
            break

    if not patch_content.strip():
        print("No patch content provided. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        patches = parse_grokpatcher_patch(patch_content)
        if not patches:
            print("No valid patches found in input.", file=sys.stderr)
            sys.exit(1)

        for header, sections in patches:
            print(f"Applying patch: {header['FromVersion']} -> {header['ToVersion']}")
            logging.info(f"Applying patch: {header['FromVersion']} -> {header['ToVersion']}")

            input_file = header["InputFile"]
            output_file = header["OutputFile"]
            target_file = header["Target"]
            
            if not os.path.exists(input_file):
                print(f"Error: Input file {input_file} does not exist", file=sys.stderr)
                logging.error(f"Input file {input_file} does not exist")
                sys.exit(1)

            # Keep a copy of the original file for revert patch
            original_content = Path(input_file).read_text(encoding="utf-8")
            original_temp = f"{input_file}.orig"
            Path(original_temp).write_text(original_content, encoding="utf-8")

            updated_content = apply_patch(input_file, sections, output_file, target_file, args.verbose)
            
            os.rename(output_file, target_file)
            print(f"Patches complete. Renamed {output_file} to {target_file}.")

            # Generate revert patch if requested
            if args.buildRevert:
                build_revert_patch(original_temp, target_file, args.buildRevert)
                print(f"Revert patch saved to {args.buildRevert}.")

            # Clean up temporary original file
            os.remove(original_temp)

    except Exception as e:
        print(f"Error applying patch: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
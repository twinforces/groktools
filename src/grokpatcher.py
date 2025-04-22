import re
import sys
import os
import difflib
import logging
import hashlib
import requests
from pathlib import Path
from typing import Tuple, List, Dict, Optional

# Configure logging to a separate file with a header
logging.basicConfig(
    filename="grokpatcher.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
with open("grokpatcher.log", "w") as f:
    f.write("=== grokpatcher.log ===\n")

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
        line = lines[i].rstrip()  # Preserve line endings but strip trailing whitespace
        i += 1

        if not line.strip():
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
            elif line.startswith("InputSectionSHA256:"):
                current_section["InputSectionSHA256"] = line.split(":", 1)[1].strip()
            elif line.startswith("ExpectedSectionSHA256:"):
                current_section["ExpectedSectionSHA256"] = line.split(":", 1)[1].strip()
            elif line.startswith("URL:"):
                current_section["URL"] = line.split(":", 1)[1].strip()
            elif line.startswith("ChunkSize:"):
                current_section["ChunkSize"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("Content:"):
                in_content = True
                continue
            elif in_content:
                # Preserve the indentation as-is
                content_lines.append(line)

    # Handle the last section and patch
    if current_section:
        current_section["Content"] = "\n".join(content_lines).rstrip()
        sections.append(current_section)
    if current_header and sections:
        patches.append((current_header, sections))

    return patches

def _compute_sha256(content: str) -> str:
    """Computes the SHA-256 checksum of the given content."""
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

def _compute_sha256_no_whitespace(content: str) -> str:
    """Computes the SHA-256 checksum of the content with all whitespace removed."""
    no_whitespace = re.sub(r'\s+', '', content)
    return _compute_sha256(no_whitespace)

def _extract_section_content(content: str, anchor: str, anchor_type: str) -> str:
    """Extracts the content between the given anchor and the next anchor."""
    if anchor_type == "natural":
        anchor_clean = re.escape(anchor.strip())
        anchor_re = re.compile(rf"^{anchor_clean}(:)?\s*$", re.MULTILINE)
    elif anchor_type == "none":
        # For append actions with no anchor, use the entire content
        return content.strip()
    else:
        anchor_re = re.compile(rf"^# ARTIFICIAL ANCHOR: {re.escape(anchor)}$", re.MULTILINE)

    match = anchor_re.search(content) if anchor_type != "none" else type('Match', (), {'start': lambda: 0, 'end': lambda: 0})()
    if not match:
        logging.error(f"Anchor '{anchor}' not found in content")
        raise ValueError(f"Anchor '{anchor}' not found in content")

    start_pos = match.end()
    next_anchor = re.compile(r"^(# ARTIFICIAL ANCHOR: .+|def\s+\w+\s*\(.*\):|if\s+.*:|\s*for\s+.*:|\s*while\s+.*:|\s*class\s+\w+\s*:)", re.MULTILINE)
    next_match = next_anchor.search(content, start_pos)
    end_pos = next_match.start() if next_match else len(content)

    section_content = content[start_pos:end_pos].strip()
    return section_content

def apply_patch(input_file: str, patches: List[Dict[str, str]], output_file: str, target_file: str, base_dir: str = "", verbose: bool = False) -> str:
    """Apply patches to the input file and return the updated content."""
    try:
        # Construct the full path to the input file using base_dir
        input_path = os.path.join(base_dir, input_file) if base_dir else input_file
        
        if not os.path.exists(input_path):
            logging.error(f"Input file {input_path} does not exist")
            raise FileNotFoundError(f"Input file {input_path} does not exist")

        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Normalize line endings to \n
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        original_content = content

        for patch in patches:
            anchor = patch.get("Anchor", "none")
            action = patch["Action"]
            anchor_type = patch.get("AnchorType", "none")
            new_content = patch.get("Content", "").replace("\\`", "`")
            input_section_sha256 = patch.get("InputSectionSHA256")
            expected_section_sha256 = patch.get("ExpectedSectionSHA256")
            url = patch.get("URL")
            chunk_size = patch.get("ChunkSize", 8192)

            # Verify the input section checksum if provided
            if input_section_sha256:
                section_content = _extract_section_content(content, anchor, anchor_type)
                actual_section_sha256 = _compute_sha256(section_content)
                actual_section_sha256_no_ws = _compute_sha256_no_whitespace(section_content)
                if actual_section_sha256 != input_section_sha256:
                    # Fallback to whitespace-removed checksum
                    if actual_section_sha256_no_ws != input_section_sha256:
                        logging.error(f"Input section checksum mismatch: expected {input_section_sha256}, got {actual_section_sha256} (whitespace-removed: {actual_section_sha256_no_ws})")
                        raise ValueError(f"Input section checksum mismatch: expected {input_section_sha256}, got {actual_section_sha256}")
                    logging.info(f"Input section checksum matched after removing whitespace for anchor '{anchor}'")
                else:
                    logging.info(f"Input section checksum verified for anchor '{anchor}'")

            if action == "append":
                # Handle chunked download and append
                if not url:
                    logging.error("URL must be specified for append action")
                    raise ValueError("URL must be specified for append action")

                # Open the output file in append mode
                mode = 'ab' if os.path.exists(output_file) else 'wb'
                sha256 = hashlib.sha256()
                with open(output_file, mode) as f:
                    response = requests.get(url, stream=True)
                    response.raise_for_status()
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:  # Filter out keep-alive chunks
                            f.write(chunk)
                            sha256.update(chunk)

                # Verify the checksum of the downloaded content
                actual_sha256 = sha256.hexdigest()
                if expected_section_sha256 and actual_sha256 != expected_section_sha256:
                    logging.error(f"Downloaded content checksum mismatch: expected {expected_section_sha256}, got {actual_sha256}")
                    raise ValueError(f"Downloaded content checksum mismatch: expected {expected_section_sha256}, got {actual_sha256}")
                logging.info(f"Downloaded content checksum verified: {actual_sha256}")

                # Since append doesn't modify the input content directly, continue to the next patch
                continue

            # Determine if the anchor is a regex pattern (enclosed in /.../)
            if anchor.startswith("/") and anchor.endswith("/"):
                anchor_pattern = anchor[1:-1]  # Remove the /.../ delimiters
                anchor_re = re.compile(anchor_pattern, re.MULTILINE)
            else:
                # For artificial anchors, match exactly with the prefix
                if anchor_type == "artificial":
                    anchor_re = re.compile(rf"^# ARTIFICIAL ANCHOR: {re.escape(anchor)}$", re.MULTILINE)
                elif anchor_type == "none":
                    # For append actions with no anchor, skip anchor matching
                    continue
                else:
                    # For natural anchors, use looser matching (ignore whitespace, optional colon)
                    anchor_clean = re.escape(anchor.strip())
                    anchor_re = re.compile(rf"^{anchor_clean}(:)?\s*$", re.MULTILINE)
            
            # Debug: Log the regex and file content
            logging.debug(f"Attempting to match anchor '{anchor}' with regex: {anchor_re.pattern}")
            logging.debug(f"File content:\n{content}")

            match = anchor_re.search(content)
            if not match:
                logging.error(f"{anchor_type.capitalize()} anchor '{anchor}' not found in {input_path}")
                raise ValueError(f"{anchor_type.capitalize()} anchor '{anchor}' not found in {input_path}")
            
            start_pos = match.start()
            next_anchor = re.compile(r"^(# ARTIFICIAL ANCHOR: .+|def\s+\w+\s*\(.*\):|if\s+.*:|\s*for\s+.*:|\s*while\s+.*:|\s*class\s+\w+\s*:)", re.MULTILINE)
            next_match = next_anchor.search(content, match.end())
            end_pos = next_match.start() if next_match else len(content)
            
            if action == "replace":
                if anchor_type == "artificial":
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

            # Verify the expected section checksum if provided
            if expected_section_sha256:
                updated_section_content = _extract_section_content(content, anchor, anchor_type)
                actual_section_sha256 = _compute_sha256(updated_section_content)
                actual_section_sha256_no_ws = _compute_sha256_no_whitespace(updated_section_content)
                if actual_section_sha256 != expected_section_sha256:
                    # Fallback to whitespace-removed checksum
                    if actual_section_sha256_no_ws != expected_section_sha256:
                        logging.error(f"Expected section checksum mismatch: expected {expected_section_sha256}, got {actual_section_sha256} (whitespace-removed: {actual_section_sha256_no_ws})")
                        raise ValueError(f"Expected section checksum mismatch: expected {expected_section_sha256}, got {actual_section_sha256}")
                    logging.info(f"Expected section checksum matched after removing whitespace for anchor '{anchor}'")
                else:
                    logging.info(f"Expected section checksum verified for anchor '{anchor}'")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Patched file written to {output_file}")
        print(f"Patched file written to {output_file}")

        # Log diff if verbose
        if verbose:
            original_lines = original_content.splitlines()
            updated_lines = content.splitlines()
            diff = list(difflib.unified_diff(original_lines, updated_lines, fromfile=input_path, tofile=output_file))
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
        # Log the contents of the files for debugging
        original_content = Path(original_file).read_text(encoding="utf-8")
        updated_content = Path(updated_file).read_text(encoding="utf-8")
        logging.debug(f"Original file content ({original_file}):\n{original_content}")
        logging.debug(f"Updated file content ({updated_file}):\n{updated_content}")

        from patchBuilder import PatchBuilder
        builder = PatchBuilder(updated_file, updated_file, original_file)
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
    parser.add_argument("--base-dir", type=str, default="", help="Base directory containing the target files.")
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
            expected_sha256 = header.get("ExpectedSHA256", None)
            
            # Construct the full path to the input file using base_dir
            input_path = os.path.join(args.base_dir, input_file) if args.base_dir else input_file
            if not os.path.exists(input_path):
                print(f"Error: Input file {input_path} does not exist", file=sys.stderr)
                logging.error(f"Input file {input_path} does not exist")
                sys.exit(1)

            # Keep a copy of the original file for revert patch
            original_content = Path(input_path).read_text(encoding="utf-8")
            original_temp = f"{input_path}.orig"
            Path(original_temp).write_text(original_content, encoding="utf-8")

            updated_content = apply_patch(input_file, sections, output_file, target_file, base_dir=args.base_dir, verbose=args.verbose)
            
            # Verify the checksum if provided
            if expected_sha256:
                actual_sha256 = _compute_sha256(updated_content)
                actual_sha256_no_ws = _compute_sha256_no_whitespace(updated_content)
                if actual_sha256 != expected_sha256:
                    # Fallback to whitespace-removed checksum
                    if actual_sha256_no_ws != expected_sha256:
                        logging.error(f"Checksum verification failed: expected {expected_sha256}, got {actual_sha256} (whitespace-removed: {actual_sha256_no_ws})")
                        raise ValueError(f"Checksum verification failed: expected {expected_sha256}, got {actual_sha256}")
                    logging.info("Checksum verification passed after removing whitespace")
                else:
                    logging.info("Checksum verification passed")

            # Update the target file path to include base_dir
            target_path = os.path.join(args.base_dir, target_file) if args.base_dir else target_file
            os.rename(output_file, target_path)
            print(f"Patches complete. Renamed {output_file} to {target_path}.")

            # Generate revert patch if requested
            if args.buildRevert:
                build_revert_patch(original_temp, target_path, args.buildRevert)
                print(f"Revert patch saved to {args.buildRevert}.")

            # Clean up temporary original file
            os.remove(original_temp)

    except Exception as e:
        print(f"Error applying patch: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
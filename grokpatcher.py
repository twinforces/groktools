import re
import sys
import os
from pathlib import Path

def parse_grokpatcher_patch(patch_content):
    """Parse a GrokPatcher patch into header and sections."""
    patches = []
    current_section = None
    content_lines = []
    header = {}
    
    lines = patch_content.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# GrokPatcher v1.0"):
            continue
        if line.startswith("# "):
            key, value = line[2:].split(":", 1)
            header[key.strip()] = value.strip()
        elif line == "[Section]":
            if current_section:
                current_section["Content"] = "\n".join(content_lines).rstrip()
                patches.append(current_section)
            current_section = {}
            content_lines = []
        elif current_section is not None:
            if line.startswith("Anchor:"):
                current_section["Anchor"] = line.split(":", 1)[1].strip()
            elif line.startswith("AnchorType:"):
                current_section["AnchorType"] = line.split(":", 1)[1].strip()
            elif line.startswith("Action:"):
                current_section["Action"] = line.split(":", 1)[1].strip()
            elif line.startswith("Content:"):
                continue
            else:
                content_lines.append(line[4:])  # Remove 4-space indent
    
    if current_section:
        current_section["Content"] = "\n".join(content_lines).rstrip()
        patches.append(current_section)
    
    return header, patches

def apply_patch(input_file, patches, output_file, anchor_type, target_file):
    """Apply patches to the input file."""
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    for patch in patches:
        anchor = patch["Anchor"]
        action = patch["Action"]
        patch_anchor_type = patch["AnchorType"]
        # De-escape backticks
        new_content = patch["Content"].replace("\\`", "`")
        
        # Construct anchor regex based on type
        if patch_anchor_type == "natural":
            # Natural anchors: match def, if, for, while, class
            anchor_re = re.compile(rf"^{re.escape(anchor)}$", re.MULTILINE)
        else:
            anchor_re = re.compile(rf"^# ARTIFICIAL ANCHOR: {re.escape(anchor)}$", re.MULTILINE)
        
        match = anchor_re.search(content)
        if not match:
            print(f"Error: {patch_anchor_type.capitalize()} anchor '{anchor}' not found in {input_file}", file=sys.stderr)
            sys.exit(1)
        
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
            print(f"Error: Unknown action '{action}'", file=sys.stderr)
            sys.exit(1)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Patched file written to {output_file}")
    
    return content

def main():
    """Run GrokPatcher as a continuous service."""
    print("GrokPatcher v1.0 started. Paste patches (end with Ctrl+D or Ctrl+Z). Final patch terminates.")
    
    while True:
        try:
            # Read patch from stdin
            patch_content = ""
            while True:
                line = sys.stdin.readline()
                if not line:  # EOF (Ctrl+D or Ctrl+Z)
                    break
                patch_content += line
            
            if not patch_content.strip():
                print("Empty patch received. Waiting for next patch.")
                continue
            
            header, patches = parse_grokpatcher_patch(patch_content)
            print(f"Applying patch: {header['FromVersion']} -> {header['ToVersion']}")
            
            input_file = header["InputFile"]
            output_file = header["OutputFile"]
            target_file = header["Target"]
            final_patch = header["FinalPatch"].lower() == "true"
            
            if not os.path.exists(input_file):
                print(f"Error: Input file {input_file} does not exist", file=sys.stderr)
                sys.exit(1)
            
            content = apply_patch(input_file, patches, output_file, header.get("AnchorType", "artificial"), target_file)
            
            if final_patch:
                # Rename output to target file
                os.rename(output_file, target_file)
                print(f"Final patch applied. Renamed {output_file} to {target_file}. Terminating.")
                break
        
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")
            break
        except Exception as e:
            print(f"Error applying patch: {str(e)}", file=sys.stderr)
            continue

if __name__ == "__main__":
    main()
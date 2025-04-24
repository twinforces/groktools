#!/usr/bin/env python3
# diffextract.py
# Extracts the unified diff content from a .grokpatch file, ignoring trailing newlines after !GO! or !DONE!.

import sys

def extract_diff(file_path=None):
    # Read from file or stdin
    if file_path:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    # Remove trailing newlines and whitespace from each line
    lines = [line.rstrip() for line in lines]

    # Find the start of the diff (after !INPUT and !OUTPUT)
    diff_start = 0
    for i, line in enumerate(lines):
        if line.startswith('---'):
            diff_start = i
            break
        if not (line.startswith('!INPUT:') or line.startswith('!OUTPUT:')):
            print(f"Error: Expected !INPUT or !OUTPUT, found: {line}", file=sys.stderr)
            sys.exit(1)

    if diff_start == 0:
        print("Error: No diff content found (missing --- line)", file=sys.stderr)
        sys.exit(1)

    # Find the end of the diff (at !GO! or !DONE!)
    diff_end = len(lines)
    for i in range(diff_start, len(lines)):
        if lines[i] in ['!GO!', '!DONE!']:
            diff_end = i
            break

    if diff_end == len(lines):
        print("Error: No !GO! or !DONE! marker found", file=sys.stderr)
        sys.exit(1)

    # Extract the diff content
    diff_lines = lines[diff_start:diff_end]

    # Output the diff content without trailing newlines
    for line in diff_lines:
        print(line)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        extract_diff(sys.argv[1])
    else:
        extract_diff()
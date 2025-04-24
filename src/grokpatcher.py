#!/usr/bin/env python3
# grokpatcher.py
# Applies patches from a .grokpatch file using gpatch with the format: gpatch <input> <diff> -o <output>.

import subprocess
import sys
import os

def apply_patch(input_file, output_file, diff_file, reverse=False):
    # Construct the gpatch command: gpatch <input> <diff> -o <output>
    cmd = ['gpatch', input_file, diff_file, '-o', output_file]
    if reverse:
        cmd.append('-R')

    try:
        # Run gpatch with verbose output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to apply patch: {e}", file=sys.stderr)
        print(f"gpatch stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def process_grokpatch(grokpatch_file):
    with open(grokpatch_file, 'r') as f:
        lines = f.readlines()

    # Extract !INPUT and !OUTPUT
    input_file = None
    output_file = None
    for line in lines:
        if line.startswith('!INPUT:'):
            input_file = line[len('!INPUT:'):].strip()
        elif line.startswith('!OUTPUT:'):
            output_file = line[len('!OUTPUT:'):].strip()
        if input_file and output_file:
            break

    if not input_file or not output_file:
        print("Error: Missing !INPUT or !OUTPUT in .grokpatch file", file=sys.stderr)
        sys.exit(1)

    # Extract the diff content (between --- and !GO! or !DONE!)
    diff_start = 0
    diff_end = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('---'):
            diff_start = i
            break
    for i in range(diff_start, len(lines)):
        if line.strip() in ['!GO!', '!DONE!']:
            diff_end = i
            break

    if diff_start == 0 or diff_end == len(lines):
        print("Error: Invalid .grokpatch format (missing diff or marker)", file=sys.stderr)
        sys.exit(1)

    # Write the diff to a temporary file
    diff_content = ''.join(lines[diff_start:diff_end])
    diff_file = 'temp_diff.diff'
    with open(diff_file, 'w') as f:
        f.write(diff_content)

    # Apply the patch
    apply_patch(input_file, output_file, diff_file)

    # Clean up the temporary diff file
    os.remove(diff_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: grokpatcher.py <grokpatch_file>", file=sys.stderr)
        sys.exit(1)

    grokpatch_file = sys.argv[1]
    if not os.path.exists(grokpatch_file):
        print(f"Error: File {grokpatch_file} does not exist", file=sys.stderr)
        sys.exit(1)

    process_grokpatch(grokpatch_file)
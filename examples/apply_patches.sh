#!/bin/bash

# apply_patches.sh
# Automates applying groktools example patches using pbcopy and grokpatcher.py.

# Ensure we're in the groktools repository root
if [ ! -d "src" ] || [ ! -d "examples" ]; then
    echo "Error: Please run this script from the groktools repository root."
    exit 1
fi

# Check for Python
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
fi

# List of patches in order
PATCHES=(
    "examples/patch_example_1.0_to_1.1.grokpatch"
    "examples/patch_example_1.1_to_1.2.grokpatch"
    "examples/patch_another_2.0_to_2.1.grokpatch"
    "examples/patch_another_2.1_to_2.2.grokpatch"
)

for patch in "${PATCHES[@]}"; do
    if [ ! -f "$patch" ]; then
        echo "Error: Patch file $patch not found."
        exit 1
    fi

    echo "Applying $patch..."

    # Copy patch to clipboard
    pbcopy < "$patch"
    echo "Patch copied to clipboard."

    # Start grokpatcher.py
    echo "Starting grokpatcher.py... Please paste the patch (Command + V) into the terminal and press Enter."
    python src/grokpatcher.py

    echo "Finished applying $patch."
    echo "----------------------------------------"
done

echo "All patches applied successfully."
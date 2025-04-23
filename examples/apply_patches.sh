#!/bin/bash
# apply_patches.sh
# Applies a series of .grokpatch files, generating doit.sh for manual patching.

set -e

# Create a log file for debugging
LOG_FILE=examples/apply_patches.log
date > "$LOG_FILE"

# List of .grokpatch files to apply
PATCH_FILES=(
    "examples/patch1.grokpatch"
    "examples/patch2.grokpatch"
    "examples/patchtest/second_coming_patch.grokpatch"
    "examples/patchtest/henry_v_patch.grokpatch"
    "examples/patchtest/second_coming_no_newline_patch.grokpatch"
)

# Concatenate all patch files with newline separators and check for !DONE!
echo "Processing patch files:" | tee -a "$LOG_FILE"
TEMP_FILE=$(mktemp)
for PATCH_FILE in "${PATCH_FILES[@]}"; do
    echo "Including $PATCH_FILE" | tee -a "$LOG_FILE"
    echo "Patch content:" >> "$LOG_FILE"
    cat "$PATCH_FILE" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    # Append the file content and ensure a newline
    cat "$PATCH_FILE" >> "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
done

# Check for !DONE! marker
if ! grep -q "^!DONE!" "$TEMP_FILE"; then
    echo "Error: !DONE! marker not found in patch set" | tee -a "$LOG_FILE"
    rm "$TEMP_FILE"
    exit 1
fi

# Process the concatenated patch files
cat "$TEMP_FILE" | iconv -f UTF-8 -t UTF-8 | python3 src/grokpatcher.py

# Clean up temp file
rm "$TEMP_FILE"

# Run the generated doit.sh to apply patches
if [ -f "doit.sh" ]; then
    echo "Running doit.sh to apply patches..." | tee -a "$LOG_FILE"
    echo "Contents of doit.sh:" >> "$LOG_FILE"
    cat doit.sh >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    ./doit.sh | tee -a "$LOG_FILE"
    # Preserve generated diff files for debugging
    echo "Generated diff files preserved for debugging:" | tee -a "$LOG_FILE"
    ls -l diff*.diff >> "$LOG_FILE" 2>/dev/null || echo "No diff files found" >> "$LOG_FILE"
    echo "Patch application complete" | tee -a "$LOG_FILE"
else
    echo "Error: doit.sh not generated" | tee -a "$LOG_FILE"
    exit 1
fi
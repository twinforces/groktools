#!/bin/bash
# apply_patches.sh
# Applies a series of patches defined in .grokpatch files.

# Log file
LOG_FILE="examples/apply_patches.log"
date > "$LOG_FILE"

# Ensure grokpatcher.py is available
if ! command -v src/grokpatcher.py >/dev/null 2>&1; then
    echo "Error: grokpatcher.py not found" | tee -a "$LOG_FILE"
    exit 1
fi

# List of patch files to apply
PATCH_FILES=(
    "examples/patch1.grokpatch"
    "examples/patch2.grokpatch"
    "examples/patchtest/second_coming_patch.grokpatch"
    "examples/patchtest/henry_v_patch.grokpatch"
    "examples/patchtest/second_coming_no_newline_patch.grokpatch"
    "examples/patchtest/code_change_patch.grokpatch"
    "examples/patchtest/multi_change_patch.grokpatch"
    "examples/patchtest/no_newline_multi_patch.grokpatch"
)

echo "Processing patch files:" | tee -a "$LOG_FILE"
for patch in "${PATCH_FILES[@]}"; do
    echo "Including $patch" | tee -a "$LOG_FILE"
done

# Generate doit.sh with patch commands
cat << 'DOIT' > doit.sh
#!/bin/bash
# doit.sh
# Generated script to apply patches.

set -e

DOIT

# Add patch commands to doit.sh
for i in "${!PATCH_FILES[@]}"; do
    patch_file="${PATCH_FILES[$i]}"
    diff_file="diff$((i+1)).diff"
    echo "src/diffextract.py \"$patch_file\" > \"$diff_file\"" >> doit.sh
done

echo "echo 'Running doit.sh to apply patches...' | tee -a \"$LOG_FILE\"" >> doit.sh

for i in "${!PATCH_FILES[@]}"; do
    patch_file="${PATCH_FILES[$i]}"
    diff_file="diff$((i+1)).diff"
    echo "echo 'Applying patch: src/grokpatcher.py \"$patch_file\"' | tee -a \"$LOG_FILE\"" >> doit.sh
    echo "src/grokpatcher.py \"$patch_file\" | tee -a \"$LOG_FILE\"" >> doit.sh
done

echo "echo 'Patch set completed' | tee -a \"$LOG_FILE\"" >> doit.sh
echo "echo 'Generated diff files preserved for debugging:' | tee -a \"$LOG_FILE\"" >> doit.sh
echo "ls -l diff*.diff | tee -a \"$LOG_FILE\"" >> doit.sh
echo "echo 'Patch application complete' | tee -a \"$LOG_FILE\"" >> doit.sh

chmod +x doit.sh

echo "Generated doit.sh with patch commands. Run './doit.sh' to apply patches." | tee -a "$LOG_FILE"

# Run the script to apply patches
./doit.sh
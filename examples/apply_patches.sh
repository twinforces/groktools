#!/bin/bash
# apply_patches.sh
# Applies .grokpatch files in the examples/ directory, including patchtest/ non-code patches, using grokpatcher.py.
# Supports Unicode characters with optional normalization.
# Temporarily saves extracted diff for debugging.

set -e

# Constants
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
GROKPATCHER="$PROJECT_ROOT/src/grokpatcher.py"
DIFFEXTRACT="$PROJECT_ROOT/src/diffextract.py"
LOG_FILE="$SCRIPT_DIR/apply_patches.log"
DEBUG_DIFF="$SCRIPT_DIR/debug_diff.txt"
NORMALIZE_UNICODE=0  # Set to 1 to normalize Unicode (e.g., convert ’ to ')

# Ensure prerequisites
if ! command -v pbcopy >/dev/null; then
    echo "Error: pbcopy not found (macOS required)" >&2
    exit 1
fi
if ! command -v gpatch >/dev/null; then
    echo "Error: gpatch not found (install via 'brew install gpatch' on macOS)" >&2
    exit 1
fi
if [ ! -f "$GROKPATCHER" ]; then
    echo "Error: grokpatcher.py not found at $GROKPATCHER" >&2
    exit 1
fi
if [ ! -f "$DIFFEXTRACT" ]; then
    echo "Error: diffextract.py not found at $DIFFEXTRACT" >&2
    exit 1
fi

# Setup logging
exec 3>&1  # Save stdout for piping
exec 1>>"$LOG_FILE" 2>&1
echo "$(date): Starting apply_patches.sh"

# Apply patch function
apply_patch() {
    local patch_file="$1"
    echo "$(date): Applying $patch_file" >&3
    echo "$(date): Applying $patch_file"
    if [ ! -f "$patch_file" ]; then
        echo "$(date): Warning: $patch_file not found, skipping" >&3
        echo "$(date): Warning: $patch_file not found, skipping"
        return
    fi
    # Handle Unicode: UTF-8 encoding or normalization
    if [ "$NORMALIZE_UNICODE" -eq 1 ]; then
        # Normalize Unicode (e.g., right quote ’ to straight quote ')
        diff_content=$(iconv -f UTF-8 -t UTF-8 "$patch_file" | sed "s/\’/\'/g"; echo)
        echo "$diff_content" | pbcopy
        echo "$diff_content" > "$DEBUG_DIFF"
        echo "$diff_content" | python3 "$GROKPATCHER" >&3
    else
        # Preserve Unicode with UTF-8
        diff_content=$(iconv -f UTF-8 -t UTF-8 "$patch_file"; echo)
        echo "$diff_content" | pbcopy
        echo "$diff_content" > "$DEBUG_DIFF"
        echo "$diff_content" | python3 "$GROKPATCHER" >&3
    fi
}

# Apply sample patches
PATCHES=("patch1.grokpatch" "patch2.grokpatch" "patchtest/second_coming_patch.grokpatch" "patchtest/henry_v_patch.grokpatch" "patchtest/second_coming_no_newline_patch.grokpatch")
for patch in "${PATCHES[@]}"; do
    # Check both examples/ and project root for patchtest/
    if [ -f "$SCRIPT_DIR/$patch" ]; then
        apply_patch "$SCRIPT_DIR/$patch"
    elif [ -f "$PROJECT_ROOT/$patch" ]; then
        apply_patch "$PROJECT_ROOT/$patch"
    else
        echo "$(date): Warning: $patch not found in $SCRIPT_DIR/ or $PROJECT_ROOT/, skipping" >&3
        echo "$(date): Warning: $patch not found in $SCRIPT_DIR/ or $PROJECT_ROOT/, skipping"
    fi
done

# Finalize with !DONE!
echo "!DONE!" | pbcopy
echo "!DONE!" | python3 "$GROKPATCHER" >&3

echo "$(date): Patch application complete" >&3
echo "$(date): Patch application complete"
exec 1>&3 3>&-  # Restore stdout
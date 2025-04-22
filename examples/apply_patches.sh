#!/bin/bash

# apply_patches.sh
# Automates applying groktools example patches using patchBuilder.py and grokpatcher.py,
# with verbose logging, revert patch generation, result verification, and reversion.

# Ensure we're in the groktools repository root
if [ ! -d "src" ] || [ ! -d "examples" ]; then
    echo "Error: Please run this script from the groktools repository root (e.g., 'cd groktools && examples/apply_patches.sh')."
    exit 1
fi

# Check for Python
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
fi

# Logging setup
LOG_FILE="apply_patches.log"
echo "=== apply_patches.log ===" > "$LOG_FILE"
echo "Starting patch application process at $(date)" >> "$LOG_FILE"

# List of patch stages (before -> after -> target -> output_patch)
PATCH_STAGES=(
    "examples/example_script_1.0_before.py examples/example_script_1.1_after.py examples/example_script.py examples/generated_patch_1.0_to_1.1.grokpatch"
    "examples/example_script_1.1_before.py examples/example_script_1.2_after.py examples/example_script.py examples/generated_patch_1.1_to_1.2.grokpatch"
    "examples/another_script_2.0_before.py examples/another_script_2.1_after.py examples/another_script.py examples/generated_patch_2.0_to_2.1.grokpatch"
    "examples/another_script_2.1_before.py examples/another_script_2.2_after.py examples/another_script.py examples/generated_patch_2.1_to_2.2.grokpatch"
)

# Array to store revert patches
REVERT_PATCHES=()

# Initialize target files by copying the initial before files
for stage in "${PATCH_STAGES[@]}"; do
    read before_path after_path target_path output_patch <<< "$stage"
    if [ ! -f "$target_path" ]; then
        cp "$before_path" "$target_path"
        echo "Initialized $target_path from $before_path" | tee -a "$LOG_FILE"
    fi
done

# Apply patches
for stage in "${PATCH_STAGES[@]}"; do
    # Parse stage parameters
    read before_path after_path target_path output_patch <<< "$stage"

    echo "Generating patch: $before_path -> $after_path for target $target_path" | tee -a "$LOG_FILE"
    
    # Debug: Log the command being executed
    echo "Executing: python src/patchBuilder.py \"$before_path\" \"$after_path\" \"$output_patch\" \"$target_path\"" | tee -a "$LOG_FILE"
    
    # Generate patch using patchBuilder.py, passing target_path, capturing output
    patch_builder_output=$(python src/patchBuilder.py "$before_path" "$after_path" "$output_patch" "$target_path" 2>&1)
    patch_builder_exit_code=$?
    echo "$patch_builder_output" | tee -a "$LOG_FILE"
    if [ $patch_builder_exit_code -ne 0 ]; then
        echo "Error: Failed to generate patch $output_patch. Check $LOG_FILE and patchbuilder.log for details." | tee -a "$LOG_FILE"
        echo "PatchBuilder output: $patch_builder_output" | tee -a "$LOG_FILE"
        exit 1
    fi

    # Update the Target and InputFile in the patch to match the target_path
    patch_content=$(cat "$output_patch")
    updated_patch_content=$(echo "$patch_content" | sed "s/# Target: .*/# Target: $(basename \"$target_path\")/" | sed "s/# InputFile: .*/# InputFile: $(basename \"$target_path\")/")
    echo "$updated_patch_content" > "$output_patch"

    # Debug: Log the patch content after modification
    echo "Patch content after sed modification:" | tee -a "$LOG_FILE"
    cat "$output_patch" | tee -a "$LOG_FILE"
    
    # Copy patch to clipboard with a newline
    echo -e "$(cat \"$output_patch\")\n" | pbcopy
    echo "Patch copied to clipboard." | tee -a "$LOG_FILE"

    # Start grokpatcher.py with --verbose, --buildRevert, and --base-dir, capturing output
    echo "Starting grokpatcher.py with --verbose, --buildRevert, and --base-dir... Please paste the patch (Command + V) into the terminal." | tee -a "$LOG_FILE"
    revert_patch="${output_patch%.grokpatch}_revert.grokpatch"
    patch_output=$(python src/grokpatcher.py --verbose --buildRevert "$revert_patch" --base-dir "examples" < "$output_patch" 2>&1)
    patch_exit_code=$?
    echo "$patch_output" | tee -a "$LOG_FILE"
    if [ $patch_exit_code -ne 0 ]; then
        echo "Error: Failed to apply patch $output_patch. Check $LOG_FILE and grokpatcher.log for details." | tee -a "$LOG_FILE"
        echo "GrokPatcher output: $patch_output" | tee -a "$LOG_FILE"
        exit 1
    fi

    # Store revert patch for later
    REVERT_PATCHES+=("$revert_patch")

    echo "Finished applying $output_patch. Revert patch saved as $revert_patch." | tee -a "$LOG_FILE"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
done

# Double-check results by comparing target files with expected after files
echo "Verifying patch results..." | tee -a "$LOG_FILE"

# Check example_script.py (should match example_script_1.2_after.py)
diff examples/example_script.py examples/example_script_1.2_after.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Verification passed: example_script.py matches expected state." | tee -a "$LOG_FILE"
else
    echo "Error: Verification failed for example_script.py. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

# Check another_script.py (should match another_script_2.2_after.py)
diff examples/another_script.py examples/another_script_2.2_after.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Verification passed: another_script.py matches expected state." | tee -a "$LOG_FILE"
else
    echo "Error: Verification failed for another_script.py. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

# Revert patches in reverse order
echo "Reverting patches..." | tee -a "$LOG_FILE"

for ((i=${#REVERT_PATCHES[@]}-1; i>=0; i--)); do
    revert_patch="${REVERT_PATCHES[$i]}"
    echo "Applying revert patch: $revert_patch" | tee -a "$LOG_FILE"
    
    # Copy revert patch to clipboard with a newline
    echo -e "$(cat \"$revert_patch\")\n" | pbcopy
    echo "Revert patch copied to clipboard." | tee -a "$LOG_FILE"

    # Start grokpatcher.py with --verbose and --base-dir, capturing output
    echo "Starting grokpatcher.py with --verbose and --base-dir... Please paste the revert patch (Command + V) into the terminal." | tee -a "$LOG_FILE"
    revert_output=$(python src/grokpatcher.py --verbose --base-dir "examples" < "$revert_patch" 2>&1)
    revert_exit_code=$?
    echo "$revert_output" | tee -a "$LOG_FILE"
    if [ $revert_exit_code -ne 0 ]; then
        echo "Error: Failed to apply revert patch $revert_patch. Check $LOG_FILE and grokpatcher.log for details." | tee -a "$LOG_FILE"
        echo "GrokPatcher output: $revert_output" | tee -a "$LOG_FILE"
        exit 1
    fi

    echo "Finished applying $revert_patch." | tee -a "$LOG_FILE"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
done

# Double-check reversion by comparing target files with original before files
echo "Verifying reversion..." | tee -a "$LOG_FILE"

# Check example_script.py (should match example_script_1.0_before.py)
diff examples/example_script.py examples/example_script_1.0_before.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Reversion passed: example_script.py matches original state." | tee -a "$LOG_FILE"
else
    echo "Error: Reversion failed for example_script.py. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

# Check another_script.py (should match another_script_2.0_before.py)
diff examples/another_script.py examples/another_script_2.0_before.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "Reversion passed: another_script.py matches original state." | tee -a "$LOG_FILE"
else
    echo "Error: Reversion failed for another_script.py. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

echo "All patches applied, verified, and reverted successfully." | tee -a "$LOG_FILE"
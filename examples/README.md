Examples for groktools Patches
This directory contains example scripts and patches demonstrating how to use groktools to maintain Python scripts with versioning, changelogs, and prompt storage. The patches are designed to be applied using grokpatcher.py from the src/ directory.
Files

example_script.py: A sample script starting at version 1.0, updated to 1.1 and 1.2 through patches.
another_script.py: A second sample script starting at version 2.0, updated to 2.1 and 2.2 through patches.
patch_example_1.0_to_1.1.grokpatch: Updates example_script.py from 1.0 to 1.1.
patch_another_2.0_to_2.1.grokpatch: Updates another_script.py from 2.0 to 2.1.
patch_example_1.1_to_1.2.grokpatch: Updates example_script.py from 1.1 to 1.2.
patch_another_2.1_to_2.2.grokpatch: Updates another_script.py from 2.1 to 2.2.
apply_patches.sh: A shell script to test applying the patches in sequence.

Prerequisites

Python 3.6+: Ensure Python is installed to run grokpatcher.py.
macOS Environment: The instructions use pbcopy for copying patch content to the clipboard, which is macOS-specific.
grokpatcher.py: Located in src/, this script applies the patches.

Applying Patches with pbcopy and grokpatcher
Each patch file updates a specific script from one version to the next. Follow these steps to apply a patch using pbcopy and grokpatcher.py:

Navigate to the Project Directory:Ensure you’re in the root of the groktools repository:
cd /path/to/groktools


Start grokpatcher.py:Run the patcher in the terminal, which will wait for patch input:
python src/grokpatcher.py


Copy the Patch to Clipboard:Use pbcopy to copy the patch content to your clipboard. For example, to apply the first patch for example_script.py:
pbcopy < examples/patch_example_1.0_to_1.1.grokpatch


Paste the Patch into grokpatcher:In the terminal running grokpatcher.py, paste the patch content:

On macOS, press Command + V to paste.
Alternatively, pipe the content directly using pbpaste:pbpaste | python src/grokpatcher.py



However, since grokpatcher.py is already running, manual pasting is typically used for sequential patches.

Apply the Patch:After pasting, grokpatcher.py will process the patch and write the updated file (e.g., example_script_1.1.py). Since the patch ends with !DONE!, it will rename the output to example_script.py and exit. Restart grokpatcher.py for the next patch.

Repeat for Each Patch:Apply the patches in sequence:

patch_example_1.0_to_1.1.grokpatch
patch_example_1.1_to_1.2.grokpatch
patch_another_2.0_to_2.1.grokpatch
patch_another_2.1_to_2.2.grokpatch



Testing with the Shell Script
The apply_patches.sh script automates applying all patches in sequence, useful for testing the full workflow:

Make the Script Executable:
chmod +x examples/apply_patches.sh


Run the Script:
./examples/apply_patches.sh



The script copies each patch to the clipboard and applies it using grokpatcher.py, pausing to allow manual pasting. Follow the on-screen instructions to paste each patch into the running grokpatcher.py instance.
Notes

Patch Order: Patches must be applied in version order (e.g., 1.0 -> 1.1, then 1.1 -> 1.2) to maintain consistency.
macOS Focus: The use of pbcopy assumes a macOS environment. For other systems (e.g., Linux), you might use xclip or directly pipe the patch file into grokpatcher.py (e.g., cat patch_file | python src/grokpatcher.py).
Restarting grokpatcher.py: Each patch file ends with !DONE!, which terminates grokpatcher.py. The shell script restarts it for each patch, but you can modify patches to use !NEXT! instead if you prefer a single session for multiple files.

For more details on the groktools suite, see the main README.md in the repository root.

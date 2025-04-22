Examples
This directory demonstrates the patching workflow for groktools, using apply_patches.sh to apply .grokpatch files to scripts and non-code files (e.g., poems in patchtest/).
Setup

Prerequisites:

Python 3.8+.
GNU diff (diff) and gpatch (gpatch):
macOS: brew install diffutils gpatch
Linux: Typically pre-installed.


pbcopy (macOS).
Ensure src/grokpatcher.py and src/diffextract.py exist.


Directory Structure:

patchtest/: Non-code patches (e.g., second_coming_patch.grokpatch, henry_v_patch.grokpatch).
Sample patches: patch1.grokpatch, patch2.grokpatch.
Sample scripts: Place scripts (e.g., script.py, SecondComing.txt) in examples/.



Running the Demo

Make Script Executable:
chmod +x apply_patches.sh


Run Demo:
./apply_patches.sh


Expected Behavior:

Applies patch1.grokpatch and patch2.grokpatch to a script (e.g., script.py), creating versions (.1, .2).
Applies patchtest/second_coming_patch.grokpatch and patchtest/henry_v_patch.grokpatch to non-code files (e.g., SecondComing.txt), handling Unicode characters (e.g., right quotation marks).
Uses !NEXT! to switch files and !DONE! to finalize.
Logs to apply_patches.log.



Unicode Handling
Non-code patches (e.g., patchtest/henry_v_patch.grokpatch) may contain Unicode characters (e.g., ’). By default, apply_patches.sh preserves these with UTF-8 encoding. To normalize (e.g., convert ’ to '), set NORMALIZE_UNICODE=1 in the script.
Notes

See docs/prompts/grokpatcher_prompt.md (Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/) for patching details.
For script details, see docs/grokpatcher.md and docs/patchBuilder.md.
Ensure sample scripts and patches exist in examples/ before running.


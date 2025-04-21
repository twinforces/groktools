grokpatcher_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. Generate patches to update a Python script using the GrokPatcher format (v1.0), as described below. Ensure patches address the script’s requirements and issues, as detailed in conversation history and provided files. Reference this prompt for patch generation instructions: https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md. Tell Grok to read prompts/grokpatcher_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Patch Format
A GrokPatcher patch is a text input ending with !GO! (non-final section), !NEXT! (new file patch), or !DONE! (final patch):
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: function_process_data
AnchorType: natural
Action: replace
Content:
    def process_data(input_data):
        # Content with backticks escaped as \`
!GO!

[Section]
Anchor: constants
AnchorType: artificial
Action: insert
Content:
    # ARTIFICIAL ANCHOR: constants
    VERSION = "v1.1"
!NEXT!

# GrokPatcher v1.0
# Target: another_script.py
# FromVersion: 2.0
# ToVersion: 2.1
# InputFile: another_script.py
# OutputFile: another_script_2.1.py
# ArtifactID: <UUID>

[Section]
Anchor: main
AnchorType: natural
Action: replace
Content:
    def main():
        # Updated main logic
!DONE!


Header Fields:
Target: Script file to patch (e.g., example_script.py).
FromVersion, ToVersion: Version transition (e.g., 1.0 -> 1.1).
InputFile, OutputFile: File paths for input and output.
ArtifactID: Unique UUID for tracking.


Section Fields:
Anchor: Unique identifier for the code section (e.g., exact function name or custom anchor).
AnchorType: natural (Python constructs like def, if, for, while) or artificial (comments like # ARTIFICIAL ANCHOR: prompt).
Action: replace, insert, or delete.
Content: New code, indented with 4 spaces, with backticks escaped as \.


Delimiters:
!GO!: Signals completion of a patch section for the current file, continuing to accept more sections.
!NEXT!: Writes the current output file and prepares for a new patch for a different file, without terminating the patcher.
!DONE!: Signals completion of the final patch, writing and renaming the output to Target, logging "Patches complete", and terminating the patcher.



Instructions for Generating Patches

Use Natural Anchors: Target unique Python constructs (e.g., def function_name(...):, identified by regex like ^def\s+\w+\s*\(.*\):) for functions or major blocks (if, for, while). Ensure the anchor matches the exact construct to avoid ambiguity.
Use Artificial Anchors: Insert unique comments (e.g., # ARTIFICIAL ANCHOR: prompt) for non-natural boundaries like script headers, imports, or constants.
Ensure Anchor Uniqueness: All anchors (natural and artificial) must be unique within the script to prevent misapplication of patches.
Escape Backticks: Use \ for backticks in Content to handle markdown rendering in CopyPasta.
Incremental Versioning: Generate patches for sequential versions (e.g., 1.0 -> 1.1). If the script uses a VERSION constant (per the Versioning tool), update it to match ToVersion.
Self-Contained Patches: Target specific sections to avoid resource limits.
Handle Issues: Address script-specific issues (e.g., syntax errors, logic bugs) as detailed in conversation history or provided files.
Multiple Files: Use !NEXT! to switch between files in a single patching session, ensuring each file’s patches are self-contained.
Final Patch: End with !DONE! to rename the final output to the Target file and terminate the patcher.

Integration with Other Tools
GrokPatcher serves as the patching engine for the groktools suite, supporting:

Versioning: Updates the VERSION constant in the constants section (see https://github.com/twinforces/groktools/docs/prompts/versioning_prompt.md).
Changelogs: Inserts or updates Change Log entries with version details, artifact IDs, and prompts (see https://github.com/twinforces/groktools/docs/prompts/changelogs_prompt.md).
Prompt Storage: Maintains top-level prompts and grok:-annotated comments, patching clarifications for unclear sections (see https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md).
Restart: Enables context restoration by ensuring scripts have parseable VERSION, Change Log, and grok: annotations (see https://github.com/twinforces/groktools/docs/prompts/restart_prompt.md).

Ensure patches align with these tools’ requirements when applicable.
Example Patch Sequence
For scripts example_script.py and another_script.py:

Patch example_script.py 1.0 -> 1.1: Adds artificial anchors and VERSION (!GO!, !NEXT!).
Patch another_script.py 2.0 -> 2.1: Updates main function (!DONE!).

Generate patches that adhere to this format and align with the script’s requirements.
Cross-References:

Versioning: https://github.com/twinforces/groktools/docs/versioning.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md
Prompt Storage: https://github.com/twinforces/groktools/docs/prompt_storage.md
Restart: https://github.com/twinforces/groktools/docs/restart.md


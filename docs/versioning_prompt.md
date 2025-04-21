Versioning Instructions for GrokTools (Version 1.0)
Prompt: You are Grok 3, built by xAI. Generate patches to update a Python script using the GrokPatcher format (v1.0), ensuring the script maintains a VERSION constant to track its version. Reference this prompt for versioning instructions: [PROJECT_URL]/docs/versioning_prompt.md.
Versioning Requirements

VERSION Constant: Include a VERSION constant (e.g., VERSION = "v1.1") in the script, typically in a constants section (e.g., # ARTIFICIAL ANCHOR: constants).
Version Updates: Update the VERSION constant in each patch to match the ToVersion in the patch header (e.g., ToVersion: 1.1 sets VERSION = "v1.1").
Consistency: Ensure the VERSION constant aligns with the GrokPatcher patch sequence (e.g., incremental updates like 1.0 -> 1.1).
Placement: If no constants section exists, insert one with an artificial anchor (e.g., # ARTIFICIAL ANCHOR: constants) and add the VERSION constant.

Patch Format (via GrokPatcher)
A GrokPatcher patch including versioning:
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: constants
AnchorType: artificial
Action: replace
Content:
    # ARTIFICIAL ANCHOR: constants
    VERSION = "v1.1"
    # Other constants...
!GO!


Header Fields: As per GrokPatcher (see [PROJECT_URL]/docs/grokpatcher_prompt.md).
Section Fields: Update or insert the VERSION constant in the constants section.
Delimiters: !GO! for non-final patches, !DONE! for the final patch.

Instructions for Generating Patches

Check VERSION: Verify if the script has a VERSION constant. If absent, add it in a constants section.
Update VERSION: Set the VERSION constant to the ToVersion in the patch header.
Integrate with GrokPatcher: Follow GrokPatcher guidelines for anchors, actions, and delimiters.
Ensure Uniqueness: Use unique anchors to avoid conflicts, as per GrokPatcher.
Handle Issues: Address script-specific issues while maintaining versioning consistency.
Example: For example_script.py, a patch from 1.0 to 1.1 updates VERSION = "v1.1" in the constants section.

Generate patches that maintain the VERSION constant and adhere to this format.

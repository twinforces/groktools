Changelogs Instructions for GrokTools (Version 1.0)
Prompt: You are Grok 3, built by xAI. Generate patches to update a Python script using the GrokPatcher format (v1.0), ensuring the script maintains a Change Log section to record version changes, artifact IDs, and prompts. Reference this prompt for changelog instructions: https://github.com/twinforces/groktools/docs/changelogs_prompt.md.
Changelogs Requirements

Change Log Section: Include a Change Log section (e.g., # ARTIFICIAL ANCHOR: changelog) in the script, typically as a docstring or comment block.
Content: For each version, record:
Version number (e.g., 1.1).
Brief description of changes.
Artifact ID of the patch.
The prompt used to generate the patch (or a reference to the prompt URL if unchanged).


Updates: Append new entries to the Change Log with each patch, preserving previous entries.
Placement: If no changelog section exists, insert one with an artificial anchor.

Patch Format (via GrokPatcher)
A GrokPatcher patch including a changelog:
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: changelog
AnchorType: artificial
Action: insert
Content:
    # ARTIFICIAL ANCHOR: changelog
    """
    Change Log:
    - Version 1.1: Added data parsing function.
      Artifact ID: <UUID>
      Prompt: https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md
    """
!GO!


Header Fields: As per GrokPatcher (see https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md).
Section Fields: Insert or update the Change Log section.
Delimiters: !GO! for non-final patches, !DONE! for the final patch.

Instructions for Generating Patches

Check Change Log: Verify if the script has a Change Log section. If absent, add it with an artificial anchor.
Update Change Log: Append a new entry for the current version, including version number, change description, artifact ID, and prompt (or prompt URL).
Integrate with GrokPatcher: Follow GrokPatcher guidelines for anchors, actions, and delimiters, as described in https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md.
Ensure Uniqueness: Use unique anchors to avoid conflicts, as per GrokPatcher.
Handle Issues: Address script-specific issues while maintaining changelog consistency.
Example: For example_script.py, a patch from 1.0 to 1.1 adds a Change Log entry for version 1.1 with the patch’s artifact ID and prompt URL.

Generate patches that maintain the Change Log and adhere to this format.

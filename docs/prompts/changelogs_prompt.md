changelogs_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. Maintain a Change Log section in a Python script to record version changes, artifact IDs, and prompts, providing traceability for script evolution. Reference this prompt for changelog instructions: https://github.com/twinforces/groktools/docs/prompts/changelogs_prompt.md. Tell Grok to read prompts/changelogs_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Changelogs Requirements

Change Log Section: Include a Change Log section (e.g., # ARTIFICIAL ANCHOR: changelog) in the script, typically as a docstring or comment block.
Content: For each version, record:
Version number (e.g., 1.1).
Brief description of changes.
Artifact ID of the change.
The prompt used to generate the change (or a reference to the prompt URL if unchanged).


Updates: Append new entries to the Change Log with each change, preserving previous entries.
Placement: If no changelog section exists, insert one with an artificial anchor.

Instructions for Maintaining Change Log

Check Change Log: Verify if the script has a Change Log section. If absent, add it with an artificial anchor.
Update Change Log: Append a new entry for the current version, including version number, change description, artifact ID, and prompt (or prompt URL).
Ensure Uniqueness: Use unique anchors for the changelog section to avoid conflicts (e.g., # ARTIFICIAL ANCHOR: changelog).
Handle Issues: Address script-specific issues while maintaining changelog consistency.
Example: For a script at version 1.0, updating to 1.1 adds a Change Log entry for version 1.1 with the change’s artifact ID and prompt URL.
Application: Use GrokPatcher to apply these changes, referencing its prompt for patch format details if needed (https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md).

Maintain the Change Log to ensure traceability of script changes.
Cross-References:

GrokPatcher: https://github.com/twinforces/groktools/docs/grokpatcher.md
Versioning: https://github.com/twinforces/groktools/docs/versioning.md
Prompt Storage: https://github.com/twinforces/groktools/docs/prompt_storage.md
Restart: https://github.com/twinforces/groktools/docs/restart.md


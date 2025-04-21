versioning_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. Maintain a VERSION constant in a Python script to track its version, updating it to match the target version in each change. Reference this prompt for versioning instructions: https://github.com/twinforces/groktools/docs/prompts/versioning_prompt.md. Tell Grok to read prompts/versioning_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Versioning Requirements

VERSION Constant: Include a VERSION constant (e.g., VERSION = "v1.1") in the script, typically in a constants section (e.g., # ARTIFICIAL ANCHOR: constants).
Version Updates: Update the VERSION constant in each change to match the target version (e.g., target version 1.1 sets VERSION = "v1.1").
Consistency: Ensure the VERSION constant aligns with the script’s version sequence (e.g., incremental updates like 1.0 -> 1.1).
Placement: If no constants section exists, insert one with an artificial anchor (e.g., # ARTIFICIAL ANCHOR: constants) and add the VERSION constant.

Instructions for Maintaining VERSION

Check VERSION: Verify if the script has a VERSION constant. If absent, add it in a constants section.
Update VERSION: Set the VERSION constant to the target version of the change.
Ensure Uniqueness: Use unique anchors for the constants section to avoid conflicts (e.g., # ARTIFICIAL ANCHOR: constants).
Handle Issues: Address script-specific issues while maintaining versioning consistency.
Example: For a script at version 1.0, updating to 1.1 sets VERSION = "v1.1" in the constants section.
Application: Use GrokPatcher to apply these changes, referencing its prompt for patch format details if needed (https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md).

Maintain the VERSION constant to reflect the script’s current version.
Cross-References:

GrokPatcher: https://github.com/twinforces/groktools/docs/grokpatcher.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md
Prompt Storage: https://github.com/twinforces/groktools/docs/prompt_storage.md
Restart: https://github.com/twinforces/groktools/docs/restart.md


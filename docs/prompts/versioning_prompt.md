Versioning Prompt
Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/
This prompt directs Grok to manage the VERSION constant in Python scripts for groktools projects to track script versions, as a Grok-side tool prompt in the Grok programming language.
Instructions

Locate or Add VERSION:

Find or insert a VERSION constant at the script’s top.
Example:VERSION = "1.0"




Increment VERSION:

Update VERSION for script changes (e.g., 1.0 to 1.1) using semantic versioning (major.minor.patch).


Ensure Consistency:

Format as a string (e.g., "1.1").
Place at script top.



Notes

Apply this prompt for versioning, independent of annotations or patching.
The patching system (grokpatcher.py, patchBuilder.py, diffextract.py) facilitates versioning by automating script updates; see docs/prompts/grokpatcher_prompt.md.
For quality checks during code regeneration, see docs/prompts/prompt_storage_prompt.md.
For changelogs, see docs/prompts/changelogs_prompt.md.
For human-readable details, see docs/versioning.md.


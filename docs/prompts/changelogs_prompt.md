Changelogs Prompt
This prompt directs Grok to update the Change Log section in Python scripts for groktools projects, ensuring a traceable history of modifications as a Grok-side tool prompt in the Grok programming language.
Instructions

Locate or Create Change Log:

Find or add a Change Log section as a comment block.

Example:
# Change Log:
# - Initial version, artifact ID: 1234




Append New Entry:

Add a brief description and artifact ID for the update.

Example:
# Change Log:
# - Initial version, artifact ID: 1234
# - Added feature, artifact ID: 5678




Maintain Consistency:

Use bullet points and include artifact IDs, avoiding duplicates.



Notes

Apply this prompt to update Change Logs, independent of versioning or patching.
The patching system (grokpatcher.py, patchBuilder.py, diffextract.py) facilitates changelog updates by automating script modifications.
For human-readable details, see docs/changelogs.md.


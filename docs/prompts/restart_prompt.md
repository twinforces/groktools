Restart Prompt
Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/
This prompt directs Grok to parse grok:-annotated comments in Python scripts for groktools projects to restore context, as a Grok-side tool prompt in the Grok programming language.
Instructions

Parse Annotations:

Read grok: (single-line) and grok: <multi-line prompt> :krog (multi-line) annotations to extract prompts and Insights.

Example:
# grok: Process dataset with pandas
# grok: Detailed instructions :krog
# Group by category, compute aggregates
# Save output as CSV
# :krog
# grok: fileref: docs/dataset_schema.md




Handle fileref::

Fetch fileref: files if in workspace, or prompt user to upload (e.g., “Please upload dataset_schema.md”).
Use file content to enrich context.


Restore Context:

Use extracted prompts, Insights, and fileref: content to reconstruct conversation state for regeneration or interaction.



Notes

Annotations are created via docs/prompts/prompt_storage_prompt.md, a Grok-side tool prompt.
For human-readable details, see docs/restart.md.


Prompt Storage Prompt
Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/
This prompt directs Grok to embed grok:-annotated comments in Python scripts for groktools projects to store prompts for regenerating source code blocks and restoring context, as a Grok-side tool prompt in the Grok programming language.
Instructions

Add Single-Line Annotations:

Use grok: to store concise prompts or user-provided Insights for regenerating the associated code block.

Example:
# grok: Process dataset with pandas, group by category
import pandas as pd




Add Multi-Line Annotations:

Use grok: <multi-line prompt> :krog to store detailed prompts or Insights for regenerating complex code blocks.

Example:
# grok: Analyze dataset and save output :krog
# Group by category, compute aggregates
# Save results as CSV
# :krog
df = pd.read_csv('data.csv')




Use fileref::

Reference external files with fileref: to provide context for regeneration.

Prompt user to upload the file if not in the workspace.

Example:
# grok: fileref: docs/dataset_schema.md
# Prompt: Please upload dataset_schema.md if not in workspace




Include Insights:

Embed user-provided Insights (e.g., instructions, context) in annotations to guide regeneration.


Quality Check:

Compare generated code with existing code.
Embed the prompt used for generation in the annotation.
If differences are detected, prompt user: “Generated code differs from existing code. Please clarify intended changes or confirm update.”


Ensure Consistency:

Format annotations clearly and consistently.



Notes

Annotations enable context restoration via docs/prompts/restart_prompt.md, a Grok-side tool prompt.
For human-readable details, see docs/prompt_storage.md.


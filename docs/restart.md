Restart
Restart is a tool in groktools that bootstraps Grok’s conversations by parsing grok:-annotated comments in Python scripts. It restores context for seamless collaboration.
Overview

Purpose: Restore Grok’s context by parsing grok: (single-line) and grok: <multi-line prompt> :krog (multi-line) annotations, enabling self-bootstrapping scripts.
Mechanism: Reads grok: and grok: <multi-line prompt> :krog comments to reconstruct conversation state.
Usage: Integrated with Prompt Storage to resume Grok’s interactions.

Usage

Ensure grok: Annotations:

Scripts must contain grok: (single-line) or grok: <multi-line prompt> :krog (multi-line) comments for context (see docs/prompt_storage.md).
Example:# grok: Process this dataset with pandas
# grok: Detailed instructions for data processing :krog
# Analyze the dataset using pandas and group by category
# Ensure output is saved as CSV
# :krog
# grok: fileref: dataset_schema.md
import pandas as pd




Run Restart Tool:

Use the Restart tool via docs/prompts/restart_prompt.md, a Grok-side tool prompt, to parse annotations.
Grok reads grok: and grok: <multi-line prompt> :krog comments to restore context, typically by reading docs/prompts/restart_prompt.md and the attached script.



Workflow

Annotation: Embed grok: or grok: <multi-line prompt> :krog comments in scripts during development.
Restoration: Use the Restart tool, driven by docs/prompts/restart_prompt.md, to parse annotations and bootstrap Grok.

Notes

The Restart tool relies on grok: and grok: <multi-line prompt> :krog annotations from Prompt Storage. See docs/prompt_storage.md for details on embedding annotations using docs/prompts/prompt_storage_prompt.md, followed by context restoration with docs/prompts/restart_prompt.md.
For related patching tools, see docs/grokpatcher.md and docs/patchBuilder.md.


Restart
Restart is a tool in groktools that bootstraps Grok’s conversations by parsing grok:-annotated comments in Python scripts. It restores context for seamless collaboration, with optional Change Log enhancement to track updates.
Overview

Purpose: Restore Grok’s context by parsing grok: (single-line) and grok: <multi-line prompt> :krog (multi-line) annotations, enabling self-bootstrapping scripts.
Mechanism: Reads grok: and grok: <multi-line prompt> :krog comments to reconstruct conversation state, optionally enhancing the Change Log.
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
Grok reads grok: and grok: <multi-line prompt> :krog comments to restore context.


Optional Change Log Enhancement:

Update the Change Log section with version updates or artifact IDs via grok: annotations.
Example:# grok: Change Log: Updated to v1.1, artifact ID: 1234





Workflow

Annotation: Embed grok: or grok: <multi-line prompt> :krog comments in scripts during development.
Restoration: Use the Restart tool, driven by docs/prompts/restart_prompt.md, to parse annotations and bootstrap Grok.
Change Logging: Optionally update the Change Log via grok: or grok: <multi-line prompt> :krog annotations.

Standards

Follow docs/prompts/bestpractices.md for consistent annotation formatting, a Grok-side tool prompt in the Grok programming language.
See docs/prompts/restart_prompt.md for Grok’s interaction guidelines, a Grok-side tool prompt.

Notes

The Restart tool relies on grok: and grok: <multi-line prompt> :krog annotations from Prompt Storage.
For annotation details, see docs/prompt_storage.md.
For related patching tools, see docs/grokpatcher.md and docs/patchBuilder.md.


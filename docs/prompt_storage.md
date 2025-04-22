Prompt Storage
Prompt Storage is a mechanism in groktools for embedding grok:-annotated comments in Python scripts to store documentation and context restoration data. It enables scripts to be self-bootstrapping, allowing Grok to resume conversations seamlessly.
Overview

Purpose: Store prompts and context within scripts to support documentation and context restoration.
Mechanism: Uses grok: for single-line comments and grok: <prompt> :krog for multi-line comment blocks, with optional fileref: tags to reference external files necessary for full context.
Usage: Integrated with the Restart tool to bootstrap Grok’s context.

Usage

Add grok: Annotations:

Use grok: for single-line comments to store concise prompts or context.
Use grok: krog: to start a multi-line comment block, ending with # :krog.
Example:# grok: Process this dataset with pandas
# grok: Detailed instructions for data processing
# Analyze the dataset using pandas and group by category
# Ensure output is saved as CSV
# :krog
import pandas as pd




Reference External Files:

Use fileref: within grok: or grok: krog: to point to external documentation or prompt files necessary for grok to understand.
Example:# grok: fileref: docs/prompts/diffu_prompt.md
# grok: fileref: dataset_schema.md
# Schema details for processing
# :krog:




Context Restoration:

The Restart tool (see docs/restart.md) parses grok: and grok: krog: annotations to restore Grok’s context.



Workflow

Annotation: Add grok: or grok: <prompt> :krog comments during script development and/or instruct grok to maintain them using the prompt_storage_prompt.
Storage: Store context or reference external files with fileref:.
Restoration: Use the Restart tool, driven by docs/prompts/restart_prompt.md, to parse annotations and bootstrap Grok.

Standards

Follow docs/prompts/bestpractices.md for consistent annotation formatting, a Grok-side tool prompt in the Grok programming language.
See docs/prompts/prompt_storage_prompt.md for Grok’s interaction guidelines, a Grok-side tool prompt.

Notes

grok: and grok: :krog annotations are script-embedded and independent of docs/prompts/, though fileref: may reference prompt files.
For context restoration details, see docs/restart.md.
For related patching tools, see docs/grokpatcher.md and docs/patchBuilder.md.


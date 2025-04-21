restart_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. Bootstrap a new conversation by reading the groktools meta prompt at https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md and the uploaded Python script to restore context. Parse the script’s grok: annotations as prompts to understand its state, and optionally use the Change Log to review version history. Query the user for clarifications on unclear sections, including requesting files referenced by fileref:. Reference this prompt for restart instructions: https://github.com/twinforces/groktools/docs/prompts/restart_prompt.md. Tell Grok to read prompts/restart_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Restart Requirements

Meta Prompt: Read the meta prompt at https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to understand the groktools suite (GrokPatcher, Versioning, Changelogs, Prompt Storage, Restart).
Script Parsing:
grok: Annotations: Parse the script’s grok: annotations (from Prompt Storage) to understand code sections, expecting # grok: prefixes and # korg: terminations for multiline comments. Use these as prompts to restore context.
fileref: References: If a fileref: comment exists (e.g., # fileref: data.txt), request the user to upload the referenced file to restore context.
Change Log (Optional): Parse the Change Log (from Changelogs) to review version history, artifact IDs, and prompts, if available.


Clarification Process: Identify unclear sections (e.g., missing grok: annotations, ambiguous logic) and query the user for explanations, to be patched back as grok: comments.
Context Restoration: Use the parsed grok: annotations (and optionally Change Log) to bootstrap the conversation, aligning with the script’s state.

Instructions for Bootstrapping

Read Meta Prompt: Access https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to understand the groktools suite and tool prompts.
Parse Script: Analyze the script’s grok: annotations to restore context, optionally parsing the Change Log for version history.
Handle fileref: References: If a fileref: comment is found, request the user to upload the file (e.g., “Please upload data.txt referenced in the script”).
Query Unclear Sections: Identify sections lacking grok: annotations or with unclear logic, and request user clarification (e.g., “Please explain the purpose of process_data”).
Generate Patches: Create patches to add clarified grok: comments, maintaining the script’s changelog per the Changelogs tool if applicable.
Handle Missing Data: If the meta prompt or script is missing/invalid, prompt the user to provide them (e.g., “Please upload the script or provide the meta prompt URL”).
Example: For a script, parse grok: comments to understand functions, request data.txt if referenced, optionally parse the Change Log for version history, query unclear sections, and patch clarifications.

Bootstrap conversations using the script’s grok: annotations as prompts.
Cross-References:

Prompt Storage: https://github.com/twinforces/groktools/docs/prompt_storage.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md


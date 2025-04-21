restart (Version 1.0)
Restart is a groktools component that bootstraps new conversations by reading the groktools meta prompt and an uploaded Python script, parsing its grok: annotations to restore context, with optional enhancement from the Change Log. It primarily relies on Prompt Storage, with Changelogs as an optional enhancement. Tell Grok to read prompts/restart_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Features

Meta Prompt: Reads the meta prompt to understand the groktools suite.
Script Parsing: Analyzes the script’s grok: annotations as prompts, optionally using the Change Log for version history.
fileref: Handling: Requests files referenced by fileref: comments to restore context.
Clarification Process: Queries unclear sections and patches clarifications as grok: comments.
Context Restoration: Bootstraps conversations based on the script’s annotations.

Restart Requirements

Meta Prompt: Access https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md.
Script Parsing: Parse grok: annotations, optionally the Change Log.
fileref: Handling: Request files referenced by fileref: comments.
Clarification Process: Identify and query unclear sections, patching clarifications as grok: comments.
Context Restoration: Align with the script’s annotations.

Bootstrapping Instructions
The following instructions, hosted at https://github.com/twinforces/groktools/docs/prompts/restart_prompt.md, guide context restoration:

[Insert content from restart_prompt.md here, identical to above]

Installation

Save docs/restart.md (this documentation).
Ensure https://github.com/twinforces/groktools/docs/prompts/restart_prompt.md is accessible.

Usage
Bootstrap a conversation by uploading the script and referencing the meta prompt:

Upload the script to Grok (e.g., paste text or upload a file).
Specify the meta prompt URL: https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md.
Grok parses the script’s grok: annotations, requests fileref: files, and queries unclear sections, generating patches as needed.

Contributing

Fork the repository at https://github.com/twinforces/groktools.
Submit pull requests with new features or bug fixes.
Report issues via GitHub Issues.

License
MIT License. See https://github.com/twinforces/groktools/LICENSE for details.
Cross-References:

Prompt Storage: https://github.com/twinforces/groktools/docs/prompt_storage.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md


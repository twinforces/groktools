prompt_storage (Version 1.0)
Prompt Storage is a groktools component that ensures Python scripts maintain a top-level prompt and grok:-annotated comments to document their purpose and functionality, with a process to clarify unclear sections and patch explanations back. It integrates with Versioning, Changelogs, and Restart tools. Tell Grok to read prompts/prompt_storage_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Features

Top-Level Prompt: A docstring at the script’s top, referencing the appropriate prompt for applying changes.
grok: Annotations: Comments prefixed with # grok: to explain key functions, blocks, or complex logic, terminated with # korg: for multiline comments, with user descriptions optional.
fileref: References: Comments prefixed with # fileref: to indicate sections generated from external files, enabling context restoration via file uploads.
Clarification Process: Queries unclear sections and patches clarifications as grok: comments.

Prompt Storage Requirements

Top-Level Prompt: Include a docstring at the script’s top (e.g., """Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md.""").
grok: Annotations: Add # grok: comments before major functions, complex blocks, or unclear sections, using # korg: for multiline termination, with user descriptions optional.
fileref: References: Add # fileref: <filename> comments for sections tied to external files, to be requested during context restoration.
Clarification Process: Identify unclear sections, query the user, and patch clarifications as # grok: comments.
Updates: Maintain and expand annotations with each change, ensuring 3am clarity for coders.

Instructions for Maintaining Prompt Storage
The following instructions, hosted at https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md, guide prompt storage maintenance:

[Insert content from prompt_storage_prompt.md here, identical to above]

Installation

Save docs/prompt_storage.md (this documentation).
Ensure https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md is accessible.

Usage
Apply changes to update prompts and annotations using GrokPatcher, as described in grokpatcher.md. Verify the top-level prompt and grok: annotations in the script after applying changes.
Contributing

Fork the repository at https://github.com/twinforces/groktools.
Submit pull requests with new features or bug fixes.
Report issues via GitHub Issues.

License
MIT License. See https://github.com/twinforces/groktools/LICENSE for details.
Cross-References:

GrokPatcher: https://github.com/twinforces/groktools/docs/grokpatcher.md
Versioning: https://github.com/twinforces/groktools/docs/versioning.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md
Restart: https://github.com/twinforces/groktools/docs/restart.md


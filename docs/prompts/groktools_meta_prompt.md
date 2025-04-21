groktools_meta_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. This meta prompt outlines the groktools suite, a set of publicly available tools for maintaining Python scripts. The suite includes five independent tools, each with a prompt and documentation, designed for general use and hosted on GitHub as a public service at https://github.com/twinforces/groktools. Tell Grok to read prompts/groktools_meta_prompt.md to use all features.
Best Practices
All code generated or modified using groktools must adhere to the best practices outlined in prompts/bestpractices.md (https://github.com/twinforces/groktools/docs/prompts/bestpractices.md). These rules ensure consistency, maintainability, and clarity, covering principles like DRY (Don’t Repeat Yourself), proper naming or commenting, declaring constants, and precompiling regexes. Refer to this document before applying any changes to scripts.
GrokTools Suite

GrokPatcher:

Purpose: A patching system for applying script updates using natural and artificial anchors, with !GO!, !NEXT!, and !DONE! delimiters.
Prompt: https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md
Doc: https://github.com/twinforces/groktools/docs/grokpatcher.md
Description: Enables precise, incremental updates to Python scripts, ensuring robust patching with unique anchors and serving as the mechanism to apply changes for other tools.


Versioning:

Purpose: Maintains a VERSION constant in scripts to track version changes.
Prompt: https://github.com/twinforces/groktools/docs/prompts/versioning_prompt.md
Doc: https://github.com/twinforces/groktools/docs/versioning.md
Description: Ensures scripts reflect their current version, supporting consistent versioning across updates.


Changelogs:

Purpose: Maintains a Change Log section in scripts to record version numbers, change descriptions, artifact IDs, and prompts.
Prompt: https://github.com/twinforces/groktools/docs/prompts/changelogs_prompt.md
Doc: https://github.com/twinforces/groktools/docs/changelogs.md
Description: Provides traceability for script evolution, documenting each update’s purpose and context.


Prompt Storage:

Purpose: Maintains a top-level prompt and grok:-annotated comments in scripts, with a process to clarify unclear sections and patch explanations back, including fileref: for external file references.
Prompt: https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md
Doc: https://github.com/twinforces/groktools/docs/prompt_storage.md
Description: Enhances script documentation, ensuring clear, maintainable code with user-verified explanations, using # korg: for multiline termination.


Restart:

Purpose: Bootstraps new conversations by reading the meta prompt and a script, parsing grok: annotations to restore context, with optional enhancement from the Change Log.
Prompt: https://github.com/twinforces/groktools/docs/prompts/restart_prompt.md
Doc: https://github.com/twinforces/groktools/docs/restart.md
Description: Enables seamless continuation of script maintenance by re-establishing context from grok: annotations.



Usage

Generate Changes: Follow each tool’s prompt for specific instructions, ensuring compliance with bestpractices.md.
Apply Changes: Use GrokPatcher to apply changes, as described in grokpatcher.md.
Bootstrap Conversations: Use the Restart tool by uploading a script and referencing this meta prompt.
Reference Prompts:
GrokPatcher: For applying changes.
Versioning: For VERSION constant updates.
Changelogs: For Change Log maintenance.
Prompt Storage: For prompt and annotation management.
Restart: For context restoration.


GitHub Repository: All tools, documentation, and prompts are available at https://github.com/twinforces/groktools.

This meta prompt serves as a central reference for the groktools suite, ensuring seamless integration and public accessibility.

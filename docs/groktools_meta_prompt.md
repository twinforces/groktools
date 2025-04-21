GrokTools Meta Prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. This meta prompt outlines the groktools suite, a set of publicly available tools for maintaining Python scripts. The suite includes five independent tools, each with a prompt and documentation, designed for general use and hosted on GitHub as a public service at [PROJECT_URL].
GrokTools Suite

GrokPatcher:

Purpose: A patching system for applying script updates using natural and artificial anchors, with !GO! and !DONE! delimiters.
Prompt: [PROJECT_URL]/docs/grokpatcher_prompt.md
Doc: [PROJECT_URL]/docs/GROKPATCHER.md
Description: Enables precise, incremental updates to Python scripts, ensuring robust patching with unique anchors.


Versioning:

Purpose: Maintains a VERSION constant in scripts to track version changes, aligning with GrokPatcher patches.
Prompt: [PROJECT_URL]/docs/versioning_prompt.md
Doc: [PROJECT_URL]/docs/VERSIONING.md
Description: Ensures scripts reflect their current version, supporting consistent versioning across updates.


Changelogs:

Purpose: Maintains a Change Log section in scripts to record version numbers, change descriptions, artifact IDs, and prompts.
Prompt: [PROJECT_URL]/docs/changelogs_prompt.md
Doc: [PROJECT_URL]/docs/CHANGELOGS.md
Description: Provides traceability for script evolution, documenting each update’s purpose and context.


Prompt Storage:

Purpose: Maintains a top-level prompt and grok:-annotated comments in scripts, with a process to clarify unclear sections and patch explanations back.
Prompt: [PROJECT_URL]/docs/prompt_storage_prompt.md
Doc: [PROJECT_URL]/docs/PROMPT_STORAGE.md
Description: Enhances script documentation, ensuring clear, maintainable code with user-verified explanations.


Restart:

Purpose: Bootstraps new conversations by reading the meta prompt and a script’s current version, parsing VERSION, Change Log, and grok: annotations to restore context.
Prompt: [PROJECT_URL]/docs/restart_prompt.md
Doc: [PROJECT_URL]/docs/RESTART.md
Description: Enables seamless continuation of script maintenance by re-establishing context from script state.



Usage

Generate Patches: Follow each tool’s prompt for specific instructions, using GrokPatcher to apply patches.
Apply Patches: Run grokpatcher.py as described in GROKPATCHER.md.
Bootstrap Conversations: Use the Restart tool by uploading a script and referencing this meta prompt.
Reference Prompts:
GrokPatcher: For patching instructions.
Versioning: For VERSION constant updates.
Changelogs: For Change Log maintenance.
Prompt Storage: For prompt and annotation management.
Restart: For context restoration.


GitHub Repository: All tools, documentation, and prompts are available at [PROJECT_URL].

This meta prompt serves as a central reference for the groktools suite, ensuring seamless integration and public accessibility.

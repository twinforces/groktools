Restart: A GrokTools Context Restoration System
Restart is a groktools component that bootstraps new conversations by reading the groktools meta prompt and an uploaded Python script’s current version, parsing its VERSION, Change Log, and grok: annotations to restore context. It integrates with GrokPatcher, Versioning, Changelogs, and Prompt Storage.
Features

Meta Prompt: Reads the meta prompt to understand the groktools suite.
Script Parsing: Analyzes the script’s top-level prompt, VERSION, Change Log, and grok: annotations.
Clarification Process: Queries unclear sections and patches clarifications as grok: comments.
Context Restoration: Bootstraps conversations based on the script’s state.

Restart Requirements

Meta Prompt: Access [PROJECT_URL]/docs/groktools_meta_prompt.md.
Script Parsing: Parse the script’s top-level prompt, VERSION, Change Log, and grok: annotations.
Clarification Process: Identify and query unclear sections, patching clarifications as grok: comments.
Context Restoration: Align with the script’s version and annotations.

Patch Format (via GrokPatcher)
A GrokPatcher patch for restart-related updates:
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: function_process_data
AnchorType: natural
Action: replace
Content:
    # grok: Parse input data using regex to extract fields, clarified per user input.
    # korg:
    def process_data(input_data):
        # Content with backticks escaped as \`
!GO!


Header Fields: As per GrokPatcher (see [PROJECT_URL]/docs/grokpatcher_prompt.md).
Section Fields: Add or update grok: annotations based on clarifications.
Delimiters: !GO! for non-final patches, !DONE! for the final patch.

Bootstrapping Instructions
The following instructions, hosted at [PROJECT_URL]/docs/restart_prompt.md, guide context restoration:

[Insert content from restart_prompt.md here, identical to above]

Installation

Save grokpatcher.py (GrokPatcher implementation).
Save RESTART.md (this documentation).
Ensure [PROJECT_URL]/docs/restart_prompt.md is accessible.
Ensure Python 3.6+ is installed.
No external dependencies required.

Usage
Bootstrap a conversation by uploading the script and referencing the meta prompt:

Upload the script to Grok.
Specify the meta prompt URL: [PROJECT_URL]/docs/groktools_meta_prompt.md.
Grok parses the script and queries unclear sections, generating patches as needed.

Contributing

Fork the repository at [PROJECT_URL].
Submit pull requests with new features or bug fixes.
Report issues via GitHub Issues.

License
MIT License. See [PROJECT_URL]/LICENSE for details.

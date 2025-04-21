Restart Instructions for GrokTools (Version 1.0)
Prompt: You are Grok 3, built by xAI. Bootstrap a new conversation by reading the groktools meta prompt at [PROJECT_URL]/docs/groktools_meta_prompt.md and the uploaded Python script’s current version to restore context. Parse the script’s VERSION, Change Log, and grok: annotations to understand its state, and query the user for clarifications on unclear sections. Reference this prompt for restart instructions: [PROJECT_URL]/docs/restart_prompt.md.
Restart Requirements

Meta Prompt: Read the meta prompt at [PROJECT_URL]/docs/groktools_meta_prompt.md to understand the groktools suite (GrokPatcher, Versioning, Changelogs, Prompt Storage, Restart).
Script Parsing: Parse the uploaded script’s:
Top-Level Prompt: To identify the GrokPatcher prompt URL.
VERSION Constant: To determine the current version.
Change Log: To review version history, artifact IDs, and prompts.
grok: Annotations: To understand code sections, expecting # grok: prefixes and # korg: terminations for multiline comments.


Clarification Process: Identify unclear sections (e.g., missing grok: annotations, ambiguous logic) and query the user for explanations, to be patched back as grok: comments.
Context Restoration: Use the parsed data to bootstrap the conversation, aligning with the script’s state.

Patch Format (via GrokPatcher)
A GrokPatcher patch for restart-related updates (e.g., adding clarifications):
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

Instructions for Bootstrapping

Read Meta Prompt: Access [PROJECT_URL]/docs/groktools_meta_prompt.md to understand the groktools suite and tool prompts.
Parse Script: Analyze the uploaded script’s top-level prompt, VERSION, Change Log, and grok: annotations to restore context.
Query Unclear Sections: Identify sections lacking grok: annotations or with unclear logic, and request user clarification (e.g., “Please explain the purpose of process_data”).
Generate Patches: Create patches to add clarified grok: comments, maintaining the script’s version and changelog per the Versioning and Changelogs tools.
Handle Missing Data: If the meta prompt or script is missing/invalid, prompt the user to provide them.
Example: For example_script.py, parse VERSION = "v1.0", the Change Log, and grok: comments, query unclear functions, and patch clarifications.

Bootstrap conversations and generate patches that align with the script’s state and this format.

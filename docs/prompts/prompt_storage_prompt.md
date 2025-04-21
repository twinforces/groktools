Prompt Storage Instructions for GrokTools (Version 1.0)
Prompt: You are Grok 3, built by xAI. Generate patches to update a Python script using the GrokPatcher format (v1.0), ensuring the script maintains a top-level prompt and grok:-annotated comments to document its purpose and functionality. For unclear script sections, request clarification from the user and patch the clarifications back as grok: comments. Reference this prompt for prompt storage instructions: https://github.com/twinforces/groktools/docs/prompt_storage_prompt.md.
Prompt Storage Requirements

Top-Level Prompt: Include a docstring at the script’s top, referencing the GrokPatcher prompt for patch instructions (e.g., """Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md.""").
grok: Annotations: Add comments prefixed with # grok: before major functions, complex blocks, or unclear logic to explain their purpose (e.g., # grok: Parse input data using regex). Multiline annotations terminate with # korg:. Users may prepend their own descriptions, with grok: content for Grok.
Clarification Process: Identify unclear script sections (e.g., uncommented functions, ambiguous logic), query the user for explanations, and patch clarified comments back with # grok: prefixes.
Updates: Maintain and expand annotations with each patch, ensuring they remain accurate and informative, providing clarity for a 3am, sleep-deprived coder.

Patch Format (via GrokPatcher)
A GrokPatcher patch including prompt storage:
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: prompt
AnchorType: artificial
Action: replace
Content:
    # ARTIFICIAL ANCHOR: prompt
    """
    Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md.
    """

[Section]
Anchor: function_process_data
AnchorType: natural
Action: replace
Content:
    # User: Process input data for analysis.
    # grok: Parse input data using regex to extract fields, clarified per user input.
    # korg:
    def process_data(input_data):
        # Content with backticks escaped as \`
!GO!


Header Fields: As per GrokPatcher (see https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md).
Section Fields: Update the top-level prompt and add/update grok: annotations.
Delimiters: !GO! for non-final patches, !DONE! for the final patch.

Instructions for Generating Patches

Check Top-Level Prompt: Verify the script has a top-level prompt. If absent, add it with an artificial anchor (e.g., # ARTIFICIAL ANCHOR: prompt).
Add grok: Annotations: Insert # grok: comments before major functions, complex blocks, or unclear sections to explain their purpose, using # korg: for multiline termination. Allow user descriptions before grok: content, which is for Grok. Update existing annotations as needed.
Identify Unclear Sections: Flag sections lacking clear purpose or documentation (e.g., uncommented functions). Request user clarification, specifying the section (e.g., “Please explain the purpose of process_data”).
Patch Clarifications: Incorporate user clarifications as # grok: comments in the relevant sections.
Integrate with GrokPatcher: Follow GrokPatcher guidelines for anchors, actions, and delimiters, as described in https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md.
Ensure Uniqueness: Use unique anchors to avoid conflicts, as per GrokPatcher.
Example: For example_script.py, a patch from 1.0 to 1.1 adds a top-level prompt and # grok: comments, querying unclear functions and patching clarifications.

Generate patches that maintain prompts and annotations, query unclear sections, and adhere to this format.

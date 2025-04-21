prompt_storage (Version 1.0)
Prompt Storage is a groktools component that ensures Python scripts maintain a top-level prompt and grok:-annotated comments to document their purpose and functionality, with a process to clarify unclear sections and patch explanations back. It integrates with GrokPatcher, Versioning, Changelogs, and Restart tools. Tell Grok to read prompts/prompt_storage_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Features

Top-Level Prompt: A docstring at the script’s top, referencing the GrokPatcher prompt for patch instructions.
grok: Annotations: Comments prefixed with # grok: to explain key functions, blocks, or complex logic, terminated with # korg: for multiline comments, with user descriptions optional.
Clarification Process: Queries unclear sections and patches clarifications as grok: comments.
Integration: Works with GrokPatcher’s anchor-based patching system.

Prompt Storage Requirements

Top-Level Prompt: Include a docstring at the script’s top (e.g., """Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md.""").
grok: Annotations: Add # grok: comments before major functions, complex blocks, or unclear sections, using # korg: for multiline termination, with user descriptions optional.
Clarification Process: Identify unclear sections, query the user, and patch clarifications as # grok: comments.
Updates: Maintain and expand annotations with each patch, ensuring 3am clarity for coders.

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
    Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md.
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


Header Fields: As per GrokPatcher (see https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md).
Section Fields: Update the top-level prompt and add/update grok: annotations.
Delimiters: !GO! for non-final sections, !NEXT! for new file patches, !DONE! for the final patch.

Patch Generation Instructions
The following instructions, hosted at https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md, guide prompt storage:

[Insert content from prompt_storage_prompt.md here, identical to above]

Installation

Save src/grokpatcher.py (GrokPatcher implementation).
Save docs/prompt_storage.md (this documentation).
Ensure https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md is accessible.
Ensure Python 3.6+ is installed.
No external dependencies required.

Usage
Use GrokPatcher to apply patches that update prompts and annotations:
python src/grokpatcher.py


Paste patches as described in grokpatcher.md.
Verify the top-level prompt and grok: annotations in the script after patching.

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


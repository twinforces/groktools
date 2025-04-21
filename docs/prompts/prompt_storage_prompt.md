prompt_storage_prompt (Version 1.0)
Prompt: You are Grok 3, built by xAI. Maintain a top-level prompt and grok:-annotated comments in a Python script to document its purpose and functionality, querying the user for clarifications on unclear sections and patching them back as grok: comments. If a section references an external file, include a fileref: comment and request the file during context restoration. Reference this prompt for prompt storage instructions: https://github.com/twinforces/groktools/docs/prompts/prompt_storage_prompt.md. Tell Grok to read prompts/prompt_storage_prompt.md to use this feature, or https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md to use all features.
Prompt Storage Requirements

Top-Level Prompt: Include a docstring at the script’s top, referencing the appropriate prompt for applying changes (e.g., """Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md.""").
grok: Annotations: Add comments prefixed with # grok: before major functions, complex blocks, or unclear logic to explain their purpose (e.g., # grok: Parse input data using regex). Multiline annotations terminate with # korg:. Users may prepend their own descriptions, with grok: content for Grok.
fileref: References: If a section is generated based on an external file, include a # fileref: <filename> comment (e.g., # fileref: data.txt). During context restoration, request the user to upload the referenced file.
Clarification Process: Identify unclear script sections (e.g., uncommented functions, ambiguous logic), query the user for explanations, and patch clarified comments back with # grok: prefixes.
Updates: Maintain and expand annotations with each change, ensuring they remain accurate and informative, providing clarity for a 3am, sleep-deprived coder.

Instructions for Maintaining Prompt Storage

Check Top-Level Prompt: Verify the script has a top-level prompt. If absent, add it with an artificial anchor (e.g., # ARTIFICIAL ANCHOR: prompt).
Add grok: Annotations: Insert # grok: comments before major functions, complex blocks, or unclear sections to explain their purpose, using # korg: for multiline termination. Allow user descriptions before grok: content, which is for Grok. Update existing annotations as needed.
Add fileref: References: If a section is generated based on an external file (e.g., data.txt), include a # fileref: data.txt comment. During context restoration, request the user to upload the file.
Identify Unclear Sections: Flag sections lacking clear purpose or documentation (e.g., uncommented functions). Request user clarification, specifying the section (e.g., “Please explain the purpose of process_data”).
Patch Clarifications: Incorporate user clarifications as # grok: comments in the relevant sections.
Ensure Uniqueness: Use unique anchors for the prompt section to avoid conflicts (e.g., # ARTIFICIAL ANCHOR: prompt).
Example: For a script, add a top-level prompt and # grok: comments, querying unclear functions and patching clarifications, with a # fileref: for sections tied to external files.
Insights: Take special note of prompts offered as an insight or hint as this is the human collaborating with you with real world experience.

Maintain the top-level prompt and grok: annotations to ensure script clarity and context restoration.
Cross-References:

GrokPatcher: https://github.com/twinforces/groktools/docs/grokpatcher.md
Versioning: https://github.com/twinforces/groktools/docs/versioning.md
Changelogs: https://github.com/twinforces/groktools/docs/changelogs.md
Restart: https://github.com/twinforces/groktools/docs/restart.md


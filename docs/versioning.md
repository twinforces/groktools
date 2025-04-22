Versioning
Versioning is a mechanism in groktools for tracking script versions by maintaining a VERSION constant in Python scripts. It ensures traceability and consistency across updates, independent of annotations or patching processes.
Overview

Purpose: Track script versions to maintain a clear history of changes.
Mechanism: Uses a VERSION constant (e.g., VERSION = "1.0") in scripts, incremented by Grok during version updates.
Usage: Managed by Grok via specific prompts for version control.

Usage

Add VERSION Constant:

Include a VERSION constant in scripts to track the current version.
Example:VERSION = "1.0"
def main():
    print("Hello, World!")




Increment VERSION:

Grok increments the VERSION constant (e.g., 1.0 to 1.1) when updating scripts, using docs/prompts/versioning_prompt.md or docs/prompts/groktools_meta_prompt.md.



Workflow

Version Management: Tell Grok to manage versioning by referencing docs/prompts/versioning_prompt.md or docs/prompts/groktools_meta_prompt.md.
Script Updates: Grok updates the VERSION constant as part of script modifications, independent of annotations or patching.

Notes

Versioning is orthogonal to grok: annotations, patch generation, and patch application, focusing solely on maintaining the VERSION constant.
The patching system (e.g., grokpatcher.py, patchBuilder.py, diffextract.py) makes versioning easier by automating script updates, facilitating consistent version tracking.
VERSION incrementing is handled by Grok, not user-side tools like patchBuilder.py, typically via docs/prompts/versioning_prompt.md or docs/prompts/groktools_meta_prompt.md, which are Grok-side tool prompts in the Grok programming language.
For patching details, see docs/grokpatcher.md and docs/patchBuilder.md.
For annotation details, see docs/prompt_storage.md.


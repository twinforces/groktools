Versioning: A GrokTools Version Tracking System
Versioning is a groktools component that ensures Python scripts maintain a VERSION constant to track their version, aligning with GrokPatcher patch updates. It integrates with GrokPatcher, Changelogs, Prompt Storage, and Restart tools for comprehensive script maintenance.
Features

VERSION Constant: A constant (e.g., VERSION = "v1.1") tracks the script’s version.
Incremental Updates: Updates the VERSION constant to match the ToVersion in GrokPatcher patches.
Consistency: Ensures version alignment across patch sequences.
Integration: Works with GrokPatcher’s anchor-based patching system.

Versioning Requirements

VERSION Constant: Include a VERSION constant in the script, typically in a constants section (e.g., # ARTIFICIAL ANCHOR: constants).
Version Updates: Update the VERSION constant in each patch to match the ToVersion.
Placement: If no constants section exists, insert one with an artificial anchor.

Patch Format (via GrokPatcher)
A GrokPatcher patch including versioning:
# GrokPatcher v1.0
# Target: example_script.py
# FromVersion: 1.0
# ToVersion: 1.1
# InputFile: example_script.py
# OutputFile: example_script_1.1.py
# ArtifactID: <UUID>

[Section]
Anchor: constants
AnchorType: artificial
Action: replace
Content:
    # ARTIFICIAL ANCHOR: constants
    VERSION = "v1.1"
    # Other constants...
!GO!


Header Fields: As per GrokPatcher (see https://github.com/twinforces/groktools/docs/grokpatcher_prompt.md).
Section Fields: Update or insert the VERSION constant.
Delimiters: !GO! for non-final patches, !DONE! for the final patch.

Patch Generation Instructions
The following instructions, hosted at https://github.com/twinforces/groktools/docs/versioning_prompt.md, guide versioning:

[Insert content from versioning_prompt.md here, identical to above]

Installation

Save grokpatcher.py (GrokPatcher implementation).
Save VERSIONING.md (this documentation).
Ensure https://github.com/twinforces/groktools/docs/versioning_prompt.md is accessible.
Ensure Python 3.6+ is installed.
No external dependencies required.

Usage
Use GrokPatcher to apply patches that update the VERSION constant:
python grokpatcher.py


Paste patches as described in GROKPATCHER.md.
Verify the VERSION constant in the script after patching.

Contributing

Fork the repository at https://github.com/twinforces/groktools.
Submit pull requests with new features or bug fixes.
Report issues via GitHub Issues.

License
MIT License. See https://github.com/twinforces/groktools/LICENSE for details.

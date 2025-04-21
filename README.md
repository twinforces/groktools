groktools
groktools is a suite of publicly available tools designed to make developing Python scripts with Grok bulletproof. It provides a set of utilities to maintain scripts with consistent versioning, changelogs, prompt storage, and automated patching, ensuring clarity and traceability even at 3am. Whether you’re managing complex data processing scripts like process_527_stats.py or building visualizations, groktools helps you keep your code organized, documented, and easy to update.
Features

Automated Patching: Generate and apply patches to Python scripts with patchBuilder.py and grokpatcher.py.
Version Tracking: Maintain a VERSION constant to track script versions.
Change Logging: Keep a Change Log section to record updates, artifact IDs, and prompts.
Prompt Storage: Add grok:-annotated comments for documentation and context restoration, with fileref: support for external files.
Context Restoration: Bootstrap conversations by parsing grok: annotations with the Restart tool.
Best Practices: Follow coding standards for consistency and maintainability (see bestpractices.md).

Project Structure

src/: Contains the core tools:
grokpatcher.py: Applies grokpatch files to update scripts.
patchBuilder.py: Generates grokpatch files by comparing before and after files.


docs/: Documentation for each tool (e.g., grokpatcher.md, patchBuilder.md).
docs/prompts/: Prompt files for Grok to use the tools (e.g., groktools_meta_prompt.md).
examples/: Example scripts, patches, and a script to test patching (apply_patches.sh).

Quick Start

Clone the Repository:
git clone https://github.com/twinforces/groktools.git
cd groktools


Ensure Requirements:

Python 3.6+ is installed.
No external dependencies are required beyond the standard library.


Explore the Tools:Use Grok to interact with the suite by referencing the meta prompt:

Tell Grok to read docs/prompts/groktools_meta_prompt.md to use all features.
Or cherry-pick specific tools using docs/prompts/*_prompt.md files (e.g., grokpatcher_prompt.md).


Try the Examples:The examples/ directory contains sample scripts and patches to demonstrate usage:
cd examples
chmod +x apply_patches.sh
./apply_patches.sh

Follow the instructions in examples/README.md to apply patches using pbcopy and grokpatcher.py.


Tools

GrokPatcher: Applies grokpatch files to update Python scripts using natural and artificial anchors.
PatchBuilder: Generates grokpatch files by comparing before and after versions of a script, automatically incrementing the VERSION.
Versioning: Maintains a VERSION constant to track script versions.
Changelogs: Keeps a Change Log section to record version updates and artifact IDs.
Prompt Storage: Adds grok:-annotated comments for documentation and context restoration.
Restart: Bootstraps conversations by parsing grok: annotations, with optional Change Log enhancement.

Best Practices
All code in groktools adheres to the best practices outlined in docs/prompts/bestpractices.md, including:

DRY principles
Clear naming and docstrings
Declaring constants
Precompiling regexes
Judicious use of classes and MVVM
Automated testing and error handling
Trusting data over specs
Detailed debug logging
PEP 8 formatting with black

Contributing
We welcome contributions to groktools! To contribute:

Fork the repository at https://github.com/twinforces/groktools.
Submit pull requests with new features or bug fixes (e.g., enhancing patchBuilder.py with interactive input).
Report issues via GitHub Issues.

License
MIT License. See LICENSE for details.

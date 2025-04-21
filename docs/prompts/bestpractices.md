bestpractices (Version 1.0)
This document outlines best practices for generating code within the groktools suite, ensuring consistency, maintainability, and clarity. These rules should be followed when creating or updating scripts, such as example_script.py, another_script.py, or any other scripts maintained with groktools.
Coding Rules
Follow the following rules when generating code:

DRY: Don't Repeat Yourself: Instead of repeating code, consider refactoring to a procedure or function. This reduces redundancy and makes future changes easier to manage.
Name Well or Comment: If the name of a procedure or class doesn’t describe what it does and why, add a docstring explaining its purpose and functionality. Clear naming or documentation ensures code is self-explanatory.
Declare Constants: Code evolves over time—make it easy to adapt. Declare constants for values that might change, following the DRY rule, to centralize modifications.
Precompile Regexes: Since regexes are constants, always use re.compile to prebuild them. This improves performance by avoiding repeated compilation during runtime.

Usage
When generating or modifying code, refer to these best practices to ensure high-quality output. For example, when updating process_527_stats.py, apply these rules to maintain clean, efficient, and understandable code.
These practices are referenced in the groktools Meta prompt (https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md) and should be followed in conjunction with tool-specific prompts.

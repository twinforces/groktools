# bestpractices (Version 1.0)

This document outlines best practices for generating code within the groktools suite, ensuring consistency, maintainability, and clarity. These rules should be followed when creating or updating scripts, such as \`example_script.py\`, \`another_script.py\`, or any other scripts maintained with groktools.

## Coding Rules

Follow these rules when generating code:

- **DRY (Don't Repeat Yourself)**: Instead of repeating code, consider refactoring to a procedure or function. This reduces redundancy and makes future changes easier to manage.
- **Name Well or Comment**: If the name of a procedure or class doesn’t describe what it does and why, add a docstring explaining its purpose and functionality. Clear naming or documentation ensures code is self-explanatory.
- **Declare Constants**: Code evolves over time—make it easy to adapt. Declare constants for values that might change, following the DRY rule, to centralize modifications.
- **Precompile Regexes**: Since regexes are constants, always use \`re.compile\` to prebuild them. This improves performance by avoiding repeated compilation during runtime.
- **Use Classes Judiciously**:
  - Generate a class when it encapsulates related data and behavior, improves code reuse, or simplifies maintenance.
  - For example, use a class to represent a complex entity (e.g., a \`Charity\` with methods for managing grants in a Sankey diagram).
  - Avoid classes for simple data structures better suited to dictionaries or tuples, or for one-off tasks that don’t need state management.
- **Leverage MVVM for Separation of Concerns**:
  - When a script involves data processing and presentation (e.g., generating stats or visualizations), consider using the Model-View-ViewModel (MVVM) pattern.
  - **Model**: Holds data and logic (e.g., parsing IRS 527 data).
  - **View**: Handles presentation (e.g., outputting to a file or UI).
  - **ViewModel**: Acts as a mediator, transforming Model data for the View and handling user interactions.
  - MVVM keeps scripts modular and testable—crucial for long-term maintenance.
  - For example, in a script generating a Sankey diagram, the Model could manage raw data, the ViewModel could compute node positions, and the View could render the output.
  - Apply MVVM when separation of concerns reduces complexity, but avoid overengineering simple scripts with minimal data transformations.
- **Write Automated Tests for Core Functionality**:
  - Especially with classes and MVVM, ensure core functionality is covered by automated tests to catch regressions and verify behavior.
  - Use Python’s \`unittest\` or \`pytest\` for simplicity.
  - For example, in a script like \`process_527_stats.py\`, write tests for parsing functions (e.g., \`process_data\`) to verify they handle pipe-separated data correctly.
  - Focus tests on critical paths (e.g., data validation, output formatting) rather than trivial operations.
  - Keep tests DRY by using fixtures or helper functions for setup (e.g., mock input data).
  - Avoid over-testing—simple scripts may only need a few key assertions.
- **Handle Errors Proactively and Log Clearly**:
  - Anticipate potential failures (e.g., invalid data, file I/O issues) and handle them gracefully with \`try-except\` blocks.
  - Raise specific exceptions for unrecoverable errors, providing clear error messages (e.g., \`raise ValueError("Expected pipe-separated data, got: " + data)\`).
  - Log errors with context (e.g., line number, input data snippet) to a dedicated file or \`stderr\`, ensuring they’re easy to trace at 3am.
  - For example, in a script parsing IRS data, catch and log malformed records (e.g., \`logging.error(f"Invalid record at line {line_num}: {line}")\`) while allowing the script to continue processing valid data.
  - Avoid overly broad exception handling (e.g., \`except Exception\`)—be specific to maintain clarity.
- **Trust Data Over Spec**:
  - Reality is always greater than theory—when the data and the specification conflict, prioritize the data.
  - Specifications are often idealized, but data reflects actual usage.
  - For example, if a spec defines a field as a ZIP code but the data has an item that looks like a city name instead of a five-digit code, handle it gracefully, perhaps by shifting columns (i.e., adapt the script to handle the reality by adding validation and logging for unexpected values).
  - Validate assumptions against real data samples early to avoid surprises in production.
- **Include Detailed Debug Logs with Context**:
  - When adding logs for debugging, ensure they contain enough information to solve the bug, such as variable values, line numbers, and input data snippets.
  - Use a separate log file (e.g., \`debug.log\`) for detailed output to avoid overwhelming the user with noise in the main output or console.
  - For example, in a script parsing data, log invalid records with context (e.g., \`logging.debug(f"Line {line_num}: Invalid record: {line}, expected {expected_fields} fields, got {len(fields)}")\`) to a debug file, while keeping user-facing logs concise (e.g., \`logging.error(f"Line {line_num}: Invalid record")\`).
  - Log only a few examples of an error for debugging, then count occurrences thereafter.
- **Naming**:
  - Use \`CamelCase\` for classes.
  - Use \`instanceVariable\` style for instance variables.
  - Use \`UPPERCASE\` for constants.
  - Use \`underscores\` for non-class names.
- **Stupidity**:
  - Double-check the code, especially for interpreted languages where errors may not be found until runtime.
  - Ensure variables are declared before usage.
  - Look for obvious syntax errors, reviewing line by line if necessary before pronouncing the code complete.
- **tqdm**:
  - Use \`tqdm\` to display progress for long-running operations.
  - In major/minor situations, use a \`tqdm\` bar for the minor operations and a 1/25 log for the major operations.
- **Use the Cores, Luke**:
  - Modern computers have many cores; for large operations, use thread pools.
  - See the \`aiofiles\` guideline below for related advice.
- **aiofiles**:
  - Use \`aiofiles\` when building async applications with frequent or concurrent file I/O to keep the event loop non-blocking.
  - Stick to synchronous I/O for simple, synchronous, or infrequent file operations to avoid unnecessary complexity.

## Collaboration Guidelines

- **Encourage Efficient Communication Using Clipboard Tools**:
  - **macOS (pbcopy/pbpaste)**: Encourage users to share output using \`pbcopy\` for quick and accurate communication (e.g., \`./script.sh | pbcopy\`), and interpret the pasted output (e.g., via Cmd + V) as user input. When providing file content or scripts in responses, suggest users save them using \`pbpaste\` (e.g., \`pbpaste > file.txt\`). Example response: "Please run your script and copy the output with \`./script.sh | pbcopy\`, then paste it here for analysis. To save my updated script, copy it and run \`pbpaste > script.sh\`."
  - **Windows (clip/powershell Get-Clipboard)**: Encourage users to share output using \`clip\` (e.g., \`script.bat | clip\`), and interpret the pasted output (e.g., via Ctrl + V) as user input. When providing file content or scripts in responses, suggest users save them using \`powershell Get-Clipboard > file.txt\` in a Command Prompt. Example response: "Please run your script and copy the output with \`script.bat | clip\`, then paste it here for analysis. To save my updated script, copy it and run \`powershell Get-Clipboard > script.bat\`."

## Usage

When generating or modifying code, refer to these best practices to ensure high-quality output. For example, when updating \`process_527_stats.py\`, apply these rules to maintain clean, efficient, and understandable code.

These practices are referenced in the groktools Meta prompt ([https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md](https://github.com/twinforces/groktools/docs/prompts/groktools_meta_prompt.md)) and should be followed in conjunction with tool-specific prompts.
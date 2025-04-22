Best Practices Prompt
The Best Practices prompt guides Grok in generating Python code that adheres to consistent, maintainable standards for groktools projects. It ensures code is clear, robust, and follows established conventions as part of the Grok programming language.
Instructions

DRY Principles:

Avoid code duplication by using functions, classes, or modules.
Example:def log_error(message):
    with open("error.log", "a") as f:
        f.write(f"{message}\n")




Clear Naming and Docstrings:

Use descriptive variable/function names and include docstrings.
Example:def parse_dataset(file_path):
    """Parse a dataset file and return processed data."""
    pass




Declare Constants:

Use uppercase for constants (e.g., VERSION = "1.0").
Example:MAX_RETRIES = 3




Precompile Regexes:

Compile regular expressions once for efficiency.
Example:import re
ZIP_CODE_PATTERN = re.compile(r"\d{5}")




Judicious Use of Classes and MVVM:

Use classes for complex data models, following Model-View-ViewModel patterns where applicable.
Example:class Dataset:
    def __init__(self, data):
        self.data = data




Automated Testing and Error Handling:

Include unit tests and try-except blocks for robustness.
Example:try:
    process_data()
except ValueError as e:
    log_error(str(e))




Trust Data Over Specs:

Prioritize reality (empirical data) over theory (specifications), logging issues rather than throwing exceptions to handle discrepancies gracefully.
Example:import logging
if len(data) != expected_length:
    logging.warning(f"Data length mismatch: got {len(data)}, expected {expected_length}")
    # Continue processing with available data




Detailed Debug Logging:

Log detailed information for debugging.
Example:import logging
logging.debug("Processing data: %s", data)




PEP 8 Formatting with black:

Format code using black for PEP 8 compliance.
Example:black script.py





Notes

Apply these practices when generating code for groktools projects using this Grok-side tool prompt in the Grok programming language.
For user-side patching tools, see docs/grokpatcher.md and docs/patchBuilder.md, which use diff -u and gpatch with diffextract.py for applying .grokpatch files.
For context restoration, see docs/prompt_storage.md and docs/restart.md.


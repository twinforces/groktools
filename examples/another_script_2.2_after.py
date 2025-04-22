# ARTIFICIAL ANCHOR: prompt
"""
Generate changes using GrokPatcher as described in https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md.
"""

# ARTIFICIAL ANCHOR: constants
# User: Script configuration constants.
# grok: Define script version and configuration constants.
# korg:
VERSION = "v2.2"

# ARTIFICIAL ANCHOR: changelog
"""
Change Log:
- Version 2.0: Initial version of another_script.py with main entry point.
  Artifact ID: c2d3e4f5-a6b7-8c9d-0e1f-b2c3d4e5f6a7
  Prompt: https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md
- Version 2.1: Updated main function placeholder.
  Artifact ID: a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d
  Prompt: https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md
- Version 2.2: Implemented main function to process data.
  Artifact ID: b3c4d5e6-f7a8-9b0c-1d2e-3f4a5b6c7d8e
  Prompt: https://github.com/twinforces/groktools/docs/prompts/grokpatcher_prompt.md
"""

# User: Main entry point for the script.
# grok: Execute primary script logic, processing data with example_script.
# korg:
def main():
    from example_script import process_data
    data = "field1|field2|field3"
    result = process_data(data)
    print(result)

if __name__ == "__main__":
    main()
# GrokPatcher: A Python Script Patching System

GrokPatcher is a lightweight, continuous patching system for applying updates to Python scripts, designed to handle large files and avoid resource limits. It uses natural and artificial anchors to precisely target sections of code, supports incremental versioning, and integrates with markdown environments by escaping backticks.

## Features

- **Continuous Operation**: Runs as a service, accepting patches via stdin (e.g., `pbpaste`) until a final patch terminates it.
- **Natural and Artificial Anchors**:
  - **Natural**: Python constructs like `def`, `if`, `for`, `while`, identified by regex.
  - **Artificial**: Comments (e.g., `# ARTIFICIAL ANCHOR: prompt`) for non-natural boundaries.
- **Incremental Versioning**: Supports sequences like 2.11 -&gt; 2.11.1 -&gt; 2.11.2 -&gt; 2.13.
- **Markdown Compatibility**: Escapes backticks (`) as `\` in patches, de-escaped during application.
- **Self-Contained Patches**: Each patch specifies input/output files and actions (`replace`, `insert`, `delete`).
- **Final Patch Handling**: Renames the final output to the original file and terminates.

## Patch Format

A GrokPatcher patch is a text file (or stdin input) with a header and section updates:

```plaintext
# GrokPatcher v1.0
# Target: process_527_stats.py
# FromVersion: 2.11
# ToVersion: 2.11.1
# InputFile: process_527_stats.py
# OutputFile: process_527_stats_2.11.1.py
# FinalPatch: false
# ArtifactID: <UUID>

[Section]
Anchor: function_debug_spurious_types
AnchorType: natural
Action: replace
Content:
    def debug_spurious_types(record_type, line, prev_line, next_line, input_file):
        # Content with backticks escaped as \`
```

- **Header Fields**:
  - `Target`: Script file to patch.
  - `FromVersion`, `ToVersion`: Version transition.
  - `InputFile`, `OutputFile`: File paths for this patch.
  - `FinalPatch`: `true` to rename output and terminate; `false` otherwise.
  - `ArtifactID`: Unique identifier.
- **Section Fields**:
  - `Anchor`: Anchor identifier (e.g., `function_debug_spurious_types`).
  - `AnchorType`: `natural` or `artificial`.
  - `Action`: `replace`, `insert`, or `delete`.
  - `Content`: New code, indented with 4 spaces, backticks escaped as `\`.

## Installation

1. Save the `grokpatcher.py` script (provided below).
2. Ensure Python 3.6+ is installed.
3. No external dependencies required.

## Usage

Run GrokPatcher as a continuous service:

```bash
python grokpatcher.py
```

- Paste patches into the terminal (e.g., via `pbpaste` on macOS).
- Each patch is applied, writing to the specified `OutputFile`.
- Continue pasting patches until a patch with `FinalPatch: true` is received.
- The final patch renames the output to the `Target` file and exits.

Example:

```bash
echo "<paste patch content>" | python grokpatcher.py
```

## Example Patch Sequence

To update `process_527_stats.py` from 2.11 to 2.13:

1. Apply patch 2.11 -&gt; 2.11.1 (adds artificial anchors).
2. Apply patch 2.11.1 -&gt; 2.11.2 (fixes `eof` error).
3. Apply patch 2.11.2 -&gt; 2.11.3 (enhances debugging).
4. Apply patch 2.11.3 -&gt; 2.13 (adds `--strict-email`, finalizes changes).

## Contributing

- Fork the repository on GitHub.
- Submit pull requests with new features or bug fixes.
- Report issues via GitHub Issues.

## License

MIT License. See `LICENSE` for details.
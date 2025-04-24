# Prompt for Generating Unified Diffs

This document outlines the requirements for generating unified diffs to be used in \`.grokpatch\` files.

## Requirements

- **Format**: Generate a unified diff compatible with GNU \`patch\`.
- **Context Lines**: Use 3 lines of context before and after each change, as per the default behavior of \`diff -u\`. If fewer than 3 context lines exist in the file (e.g., in a file with fewer than 3 lines), use the available lines.
- **Hunk Separation**: Multiple hunks should be separated naturally by the unchanged lines between them. Extra blank lines between hunks are not required.
- **Timestamps**: Use a fixed timestamp for reproducibility: \`2025-04-21 23:14:00.000000000 -0700\`.
- **File Paths**: Use the paths specified in the \`.grokpatch\` file’s \!INPUT and \!OUTPUT lines (e.g., \`examples/patchtest/SecondComing.txt\`).
- **No Trailing Newline**: If the file does not end with a newline, include \`\ No newline at end of file\` at the end of the diff section.

## Edge Cases

- **Empty Old Files**: For empty old files, start at line 0 in the hunk header (e.g., \`@@ -0,0 +1,2 @@\` indicates an empty old file and a new file with 2 lines).
- **Empty New Files**: For empty new files, mark all lines as removed (e.g., \`@@ -1,3 +0,0 @@\` indicates 3 lines removed from the old file, resulting in an empty new file).

## Patch Generation Best Practices

To ensure patches apply correctly and avoid common issues, follow these guidelines:

- **Verify the Source File**: Always generate diffs using the exact content of the source file as it exists in the repository. Do not rely on prior versions or memory of the file, as this can lead to mismatches in line numbers, whitespace, or content.
- **Check Line Numbers and Context**: Before generating a diff, verify the line numbers and context lines in the source file match the expected "before" state. Use tools like \`sed -n 'start,endp' filename\` to inspect specific line ranges and ensure they align with the diff’s hunk headers.
- **Handle Whitespace and Line Endings**: Ensure there are no trailing whitespace or inconsistent line endings (e.g., \`\r\n\` vs. \`\n\`). Use tools like \`cat -v\` to inspect hidden characters, and normalize line endings to Unix-style (\`\n\`) if necessary.
- **Use Consistent Tools**: Generate diffs using the \`diff -u\` command directly with the source and target files, rather than constructing diffs manually, to avoid formatting errors. Example: \`diff -u before_file after_file > patch.diff\`.
- **Test the Patch**: After generating a diff, test it on a copy of the source file using \`gpatch --dry-run\` to ensure it applies cleanly before finalizing. Example: \`gpatch --dry-run -i patch.diff source_file\`.
- **Debug Failures**: If a patch fails to apply, inspect the reject file (e.g., \`.rej\`) and use \`gpatch --verbose\` to get detailed output. Compare the failed hunk’s context with the actual file content to identify mismatches.

## Example

For a change from:

\`\`\`
Turning and turning in the widening gyre
The weasel cannot hear the wrangler;
Things fall apart; the centre cannot hold;
\`\`\`

to:

\`\`\`
Turning and turning in the widening gyre
The weasel cannot hear the wrangler's call;
Things fall apart; the centre cannot hold;
'Mere anarchy is loosed upon the world,'
\`\`\`

The unified diff should be:

\`\`\`
--- examples/patchtest/SecondComing.txt	2025-04-21 23:14:00.000000000 -0700
+++ examples/patchtest/SecondComing.txt	2025-04-21 23:14:00.000000000 -0700
@@ -1,3 +1,4 @@
 Turning and turning in the widening gyre
-The weasel cannot hear the wrangler;
+The weasel cannot hear the wrangler's call;
 Things fall apart; the centre cannot hold;
+'Mere anarchy is loosed upon the world,'
\`\`\`

Ensure the diff is minimal and does not include unnecessary context or blank lines unless required by the 3-line context rule.
diffu_prompt.md
This document describes the prompt used to generate diff -u (unified diff) patches for groktools, emulating the behavior of the diff -u command without relying on external tools. The generated patches are compatible with the patch command (specifically GNU patch, or gpatch on macOS) and follow the unified diff format as specified in RFC 9829.
Prompt Format
The following prompt instructs Grok to generate a diff -u patch by comparing two files, building an edit script, and formatting the output with the correct unified diff structure:
Generate a unified diff (`diff -u`) patch comparing two files, FILE1 and FILE2, with their contents provided below. The patch must be compatible with the `patch` command and follow the unified diff format as specified in RFC 9829. Do not use the `diff` command or any external tools; compute the diff manually using the following steps, inspired by GNU diffutils:

1. **Compare Lines**: Identify matching lines between FILE1 and FILE2 using a longest common subsequence approach. Consider lines identical if their content matches exactly (case-sensitive, including whitespace).
2. **Build Edit Script**: Create a list of changes, where each change specifies:
   - Starting line number in FILE1 (0-based).
   - Number of lines deleted from FILE1.
   - Starting line number in FILE2 (0-based).
   - Number of lines inserted from FILE2.
3. **Generate Patch**:
   - Include file headers with timestamps (use the current timestamp: April 21, 2025, 23:14 PDT), e.g., `--- file1.txt 2025-04-21 23:14:00.000000000 -0700`.
   - For each change, create a hunk with:
     - Hunk header in the format `@@ -start,count +start,count @@`, where `start` is the 1-based line number in the original/new file, and `count` is the number of lines affected (including context). If the count is 0 (e.g., empty file or range), use the line number before the range.
     - 2 lines of context before and after changes (unless at the start/end of the file).
     - Lines prefixed with `-` for deletions, `+` for additions, and a space for unchanged context lines.
   - Split into multiple hunks if there are more than 2 * 2 + 1 = 5 unchanged lines between changes, ensuring proper context.
   - Add a blank line between hunks by including an extra newline after each hunk, but only if there are multiple hunks.

FILE1 (name: "[filename1]"):
[Insert FILE1 content here]

FILE2 (name: "[filename2]"):
[Insert FILE2 content here]

Output the unified diff patch below.

Usage Notes

Context Size: The prompt uses 2 lines of context to balance patch readability and compatibility. You can adjust the context size (e.g., to 3 lines) by modifying the prompt, which changes the hunk splitting threshold to 2 * context + 1.
Compatibility: The generated patches are designed to work with GNU patch (gpatch on macOS). BSD patch (default on macOS) may misinterpret blank lines between hunks, so gpatch is recommended. See docs/patching.md for more details.
Line Endings: Ensure all patch files use Unix-style line endings (\n) to avoid compatibility issues with patch.

Example
For an example of applying this prompt, see the test script test_poem_patches.sh, which uses this prompt to generate diff -u patches for SecondComing.txt and HenryV-3-3.txt.

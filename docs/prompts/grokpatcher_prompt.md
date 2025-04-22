GrokPatcher Prompt
This prompt directs Grok to process .grokpatch files for updating Python scripts in groktools projects, as a Grok-side tool prompt in the Grok programming language.
Instructions

Base URL: https://github.com/twinforces/groktools/raw/refs/heads/master/

Generate Unified Diff:

Read docs/prompts/diffu_prompt.md to generate unified diffs for .grokpatch files.


Wrap in .grokpatch:

Add metadata: !INPUT: <path>, !OUTPUT: <path>.

Place diff after metadata.

End with !GO! as EOF marker.

Example:
!INPUT: script.py
!OUTPUT: script.py
--- script.py
+++ script.py
@@ -1,3 +1,4 @@
 def main():
     print("Hello")
-    print("World")
+    print("Grok with \`code\`")
     return
!GO!




Parse .grokpatch:

Extract metadata: !INPUT: <path>, !OUTPUT: <path>.
Extract diff (from --- to before !GO!).
Verify !GO! as EOF marker.


Validate Metadata:

Confirm input file exists at !INPUT path.


Apply Patch:

Use diffextract.py to unescape backticks and extract diff.
Apply diff with gpatch (e.g., python src/diffextract.py file.grokpatch | gpatch -p1).
Detect !DONE! to end patch set.


Handle Errors:

Log issues for invalid metadata, malformed diffs, or gpatch failures.



Notes

Use docs/prompts/diffu_prompt.md for diff generation, a Grok-side tool prompt.
User-side tools (grokpatcher.py, patchBuilder.py, diffextract.py) use diff -u and gpatch; see docs/grokpatcher.md and docs/patchBuilder.md.


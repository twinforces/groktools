Diffu Prompt
This prompt directs Grok to generate unified diffs comparing two file versions, aligned with GNU diffutils behavior (https://savannah.gnu.org/projects/diffutils), as a Grok-side tool prompt in the Grok programming language.
Instructions

Generate Unified Diff:

Compare old and new file versions.

Use headers: --- old_file and +++ new_file (no timestamps).

Use hunk markers: @@ -start,count +start,count @@ for line numbers and counts (e.g., @@ -1,3 +1,4 @@).

Prefix lines: space for unchanged (context), - for removed, + for added.

Include blank lines between hunks.

Escape backticks (e.g., ` to ```) for copypasta compatibility.

Example:
--- script.py
+++ script.py
@@ -1,3 +1,4 @@
 def main():
     print("Hello")
-    print("World")
+    print("Grok with \`code\`")
     return




Handle Edge Cases:

For empty old files, start at line 0 (e.g., @@ -0,0 +1,2 @@).
For empty new files, mark all lines as removed (e.g., @@ -1,3 +0,0 @@).
Ensure at least 3 context lines per hunk, unless fewer exist.


Ensure Compatibility:

Generate diffs compatible with gpatch.
Exclude timestamps and SHA hashes.



Notes

Validate diffs with gpatch --dry-run.


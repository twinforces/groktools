import sys
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime
import pytz
import difflib

# Configure logging
logging.basicConfig(
    filename="patchbuilder.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
with open("patchbuilder.log", "w") as f:
    f.write("=== patchbuilder.log ===\n")

class Change:
    """Represents a change in the edit script."""
    def __init__(self, line0: int, line1: int, deleted: int, inserted: int):
        self.line0 = line0
        self.line1 = line1
        self.deleted = deleted
        self.inserted = inserted
        self.link = None

class PatchBuilder:
    """Builds a diff -u patch by comparing before and after files."""
    def __init__(self, target_path: str, before_path: str, after_path: str):
        self.target = target_path
        self.before_path = before_path
        self.after_path = after_path
        self.input_file = Path(target_path).name
        self.before_lines = Path(before_path).read_text(encoding="utf-8").splitlines()
        self.after_lines = Path(after_path).read_text(encoding="utf-8").splitlines()
        self.context = 2  # Default context lines for unified diff

    def _build_edit_script(self) -> Optional[Change]:
        """Builds an edit script by comparing before and after lines."""
        matcher = difflib.SequenceMatcher(None, self.before_lines, self.after_lines)
        script = None
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                continue
            deleted = i2 - i1
            inserted = j2 - j1
            if deleted > 0 or inserted > 0:
                change = Change(i1, j1, deleted, inserted)
                change.link = script
                script = change
        return script

    def _find_hunk(self, script: Optional[Change]) -> Optional[Change]:
        """Finds the next hunk to print, splitting at large gaps of unchanged lines."""
        if not script:
            return None
        threshold = 2 * self.context + 1
        current = script
        while current:
            next_change = current.link
            if not next_change:
                return current
            top0 = current.line0 + current.deleted
            gap = next_change.line0 - top0
            if gap >= threshold:
                return current
            current = next_change
        return script

    def _print_unidiff_hunk(self, hunk: Change, before_lines: List[str], after_lines: List[str]) -> str:
        """Generates a unified diff hunk."""
        first0, last0 = hunk.line0, hunk.line0 + hunk.deleted - 1
        first1, last1 = hunk.line1, hunk.line1 + hunk.inserted - 1

        # Add context
        first0 = max(0, first0 - self.context)
        first1 = max(0, first1 - self.context)
        last0 = min(len(before_lines) - 1, last0 + self.context) if last0 + self.context < len(before_lines) else len(before_lines) - 1
        last1 = min(len(after_lines) - 1, last1 + self.context) if last1 + self.context < len(after_lines) else len(after_lines) - 1

        # Adjust line counts for unified diff (1-based, include context)
        count0 = last0 - first0 + 1 if last0 >= first0 else 0
        count1 = last1 - first1 + 1 if last1 >= first1 else 0

        # Unified diff line numbers are 1-based
        start0 = first0 + 1 if count0 > 0 else first0
        start1 = first1 + 1 if count1 > 0 else first1

        # Handle empty ranges for patch compatibility
        if count0 == 0:
            start0 = first0
        if count1 == 0:
            start1 = first1

        # Hunk header
        count0_str = f"{count0}" if count0 > 0 else "0"
        count1_str = f"{count1}" if count1 > 0 else "0"
        hunk_output = f"@@ -{start0},{count0_str} +{start1},{count1_str} @@\n"

        # Print lines
        i, j = first0, first1
        next_hunk = hunk

        while i <= last0 or j <= last1:
            if not next_hunk or i < next_hunk.line0:
                # Unchanged line from before file
                line = before_lines[i]
                hunk_output += f" {line}\n"
                i += 1
                j += 1
            else:
                # Deletions
                k = next_hunk.deleted
                while k > 0 and i <= last0:
                    line = before_lines[i]
                    hunk_output += f"-{line}\n"
                    i += 1
                    k -= 1

                # Insertions
                k = next_hunk.inserted
                while k > 0 and j <= last1:
                    line = after_lines[j]
                    hunk_output += f"+{line}\n"
                    j += 1
                    k -= 1

                next_hunk = next_hunk.link

        return hunk_output

    def build(self, output_path: Optional[str] = None) -> str:
        """Generates a diff -u patch and writes to a file if specified."""
        try:
            # File headers with timestamps
            timestamp = "2025-04-21 23:14:00.000000000 -0700"
            patch_content = f"--- {self.before_path}\t{timestamp}\n"
            patch_content += f"+++ {self.after_path}\t{timestamp}\n"

            # Build edit script
            script = self._build_edit_script()

            # Generate hunks
            current = script
            first_hunk = True
            while current:
                hunk_end = self._find_hunk(current)
                hunk_content = self._print_unidiff_hunk(current, self.before_lines, self.after_lines)
                if not first_hunk:
                    patch_content += "\n"  # Blank line between hunks
                patch_content += hunk_content
                first_hunk = False
                current = hunk_end.link

            if output_path:
                Path(output_path).write_text(patch_content, encoding="utf-8")
                logging.info(f"Unified diff patch written to {output_path}")

            return patch_content

        except Exception as e:
            logging.error(f"Failed to build unified diff patch: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to build unified diff patch: {str(e)}")

def main():
    """CLI entry point for patchBuilder.py."""
    if len(sys.argv) < 5:
        print("Usage: python patchBuilder.py <before_path> <after_path> <output_path> <target_path>")
        sys.exit(1)

    before_path = sys.argv[1]
    after_path = sys.argv[2]
    output_path = sys.argv[3]
    target_path = sys.argv[4]

    try:
        builder = PatchBuilder(target_path, before_path, after_path)
        patch_content = builder.build(output_path)
        print(f"Generated unified diff patch:\n{patch_content}")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
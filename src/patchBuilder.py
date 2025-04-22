import uuid
import logging
import sys
import re
import difflib
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Constants for grokpatch format
PATCH_HEADER = """# GrokPatcher v1.0
# Target: {target}
# FromVersion: {from_version}
# ToVersion: {to_version}
# InputFile: {input_file}
# OutputFile: {output_file}
# ArtifactID: {artifact_id}
"""
SECTION_TEMPLATE = """
[Section]
Anchor: {anchor}
AnchorType: {anchor_type}
Action: {action}
Content:
{content}
"""
DELIMITER = "!DONE!"

# Precompile regex for version string, anchors, and docstrings
VERSION_RE = re.compile(r'VERSION\s*=\s*"v(\d+)\.(\d+)"')
DEF_RE = re.compile(r'^def\s+\w+\s*\(.*\):')
ANCHOR_RE = re.compile(r'^# ARTIFICIAL ANCHOR: .+')
DOCSTRING_RE = re.compile(r'^\s*"""')

# Configure logging to a separate file
logging.basicConfig(
    filename="patchbuilder.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PatchSection:
    """Represents a single section in a grokpatch file."""
    def __init__(self, anchor: str, anchor_type: str, action: str, content: str):
        self.anchor = anchor
        self.anchor_type = anchor_type.lower()
        self.action = action.lower()
        self.content = self._format_content(content)

    def _format_content(self, content: str) -> str:
        """Formats content with 4-space indentation and escapes backticks."""
        lines = content.splitlines()
        indented_lines = ["    " + line for line in lines]
        return "\n".join(indented_lines).replace("`", "\\`")

    def to_string(self) -> str:
        """Generates the section string in grokpatch format."""
        return SECTION_TEMPLATE.format(
            anchor=self.anchor,
            anchor_type=self.anchor_type,
            action=self.action,
            content=self.content
        )

class PatchBuilder:
    """Builds a grokpatch file by comparing before and after files."""
    def __init__(self, target: str, before_path: str, after_path: str):
        self.target = target
        self.before_path = before_path
        self.after_path = after_path
        self.input_file = target
        self.sections: List[PatchSection] = []
        self.from_version, self.to_version = self._increment_version()
        # Use the target file's base name for the OutputFile
        target_base = Path(target).stem
        self.output_file = f"{target_base}_{self.to_version}.{Path(target).suffix.lstrip('.')}"
        self.artifact_id = str(uuid.uuid4())

    def _increment_version(self) -> Tuple[str, str]:
        """Finds the VERSION string in the before file, increments it, and logs the change."""
        try:
            before_content = Path(self.before_path).read_text(encoding="utf-8")
            match = VERSION_RE.search(before_content)
            if not match:
                logging.error(f"No VERSION string found in {self.before_path}")
                raise ValueError(f"No VERSION string found in {self.before_path}")

            major, minor = map(int, match.groups())
            from_version = f"v{major}.{minor}"
            to_version = f"v{major}.{minor + 1}"
            
            logging.info(f"Version incremented from {from_version} to {to_version}")
            return from_version, to_version

        except Exception as e:
            logging.error(f"Failed to increment version: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to increment version: {str(e)}")

    def add_section(self, anchor: str, anchor_type: str, action: str, content: str) -> None:
        """Adds a section to the patch, replacing any existing section with the same anchor."""
        if anchor_type not in ("natural", "artificial"):
            logging.error(f"Invalid anchor_type: {anchor_type}, must be 'natural' or 'artificial'")
            raise ValueError(f"Invalid anchor_type: {anchor_type}")
        if action not in ("replace", "insert", "delete"):
            logging.error(f"Invalid action: {action}, must be 'replace', 'insert', or 'delete'")
            raise ValueError(f"Invalid action: {action}")
        
        # Remove any existing section with the same anchor
        existing_count = sum(1 for s in self.sections if s.anchor == anchor)
        self.sections = [s for s in self.sections if s.anchor != anchor]
        logging.debug(f"Removed {existing_count} existing sections with anchor={anchor}")
        
        section = PatchSection(anchor, anchor_type, action, content)
        self.sections.append(section)
        logging.debug(f"Added section: anchor={anchor}, anchor_type={anchor_type}, action={action}")

    def generate_patch(self) -> None:
        """Generates patch sections by comparing before and after files."""
        try:
            before_lines = Path(self.before_path).read_text(encoding="utf-8").splitlines()
            after_lines = Path(self.after_path).read_text(encoding="utf-8").splitlines()

            # Update VERSION in after_lines if needed
            after_content = "\n".join(after_lines)
            if VERSION_RE.search(after_content):
                after_content = VERSION_RE.sub(f'VERSION = "{self.to_version}"', after_content)
                after_lines = after_content.splitlines()
                # Add a section for the VERSION update
                self.add_section(
                    anchor="constants",
                    anchor_type="artificial",
                    action="replace",
                    content=f'# ARTIFICIAL ANCHOR: constants\n# User: Script configuration constants.\n# grok: Define script version and configuration constants.\n# korg:\nVERSION = "{self.to_version}"'
                )

            # Use difflib to compare files
            differ = difflib.Differ()
            diff = list(differ.compare(before_lines, after_lines))

            # Group changes into sections
            current_section_lines = []
            current_action = None
            current_anchor = None
            current_anchor_type = None
            line_num = 0
            anchor_line_num = -1
            in_section = False
            in_docstring = False

            for line in diff:
                line_num += 1
                stripped_line = line[2:].strip() if line.startswith(("+ ", "- ")) else line.strip()

                # Check for docstring start/end
                if DOCSTRING_RE.match(stripped_line):
                    in_docstring = not in_docstring

                # Check for anchor lines
                is_def = DEF_RE.match(stripped_line)
                is_anchor = ANCHOR_RE.match(stripped_line)
                if (is_def or is_anchor) and not in_docstring:
                    if current_section_lines and in_section:
                        # End the previous section
                        content = "\n".join(current_section_lines)
                        if content.strip():
                            self.add_section(current_anchor, current_anchor_type, current_action, content)
                        current_section_lines = []
                        current_action = None
                        in_section = False
                    if is_def:
                        current_anchor = stripped_line.split(":", 1)[0].strip()
                        current_anchor_type = "natural"
                    else:
                        current_anchor = stripped_line.split(":", 1)[1].strip()
                        current_anchor_type = "artificial"
                    anchor_line_num = line_num

                if line.startswith("  "):  # No change
                    if current_section_lines and anchor_line_num != line_num:
                        current_section_lines.append(line[2:])
                    continue

                # Start a new section if we encounter a change
                if not current_anchor:
                    current_anchor = f"section_{line_num}"
                    current_anchor_type = "artificial"

                in_section = True

                # Determine action based on diff markers
                if line.startswith("- "):
                    if current_action is None:
                        current_action = "replace" if any(l.startswith("+ ") for l in diff[line_num-1:]) else "delete"
                    if current_action == "delete":
                        current_section_lines.append(line[2:])
                elif line.startswith("+ "):
                    if current_action is None:
                        current_action = "replace" if any(l.startswith("- ") for l in diff[:line_num]) else "insert"
                    current_section_lines.append(line[2:])

            # Add the last section if there are pending changes
            if current_section_lines and in_section:
                content = "\n".join(current_section_lines)
                if content.strip():
                    self.add_section(current_anchor, current_anchor_type, current_action, content)

        except Exception as e:
            logging.error(f"Failed to generate patch: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate patch: {str(e)}")

    def build(self, output_path: Optional[str] = None) -> str:
        """Generates the grokpatch content and optionally writes to a file."""
        try:
            patch_content = PATCH_HEADER.format(
                target=self.target,
                from_version=self.from_version,
                to_version=self.to_version,
                input_file=self.input_file,
                output_file=self.output_file,
                artifact_id=self.artifact_id
            )
            
            for section in self.sections:
                patch_content += section.to_string()
            
            patch_content += DELIMITER
            
            if output_path:
                Path(output_path).write_text(patch_content, encoding="utf-8")
                logging.info(f"Grokpatch written to {output_path}")
            
            return patch_content
        
        except Exception as e:
            logging.error(f"Failed to build grokpatch: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to build grokpatch: {str(e)}")

def main():
    """CLI entry point for patchBuilder.py."""
    if len(sys.argv) < 4:
        print("Usage: python patchBuilder.py <before_path> <after_path> <output_path>")
        sys.exit(1)

    before_path = sys.argv[1]
    after_path = sys.argv[2]
    output_path = sys.argv[3]
    target = Path(before_path).name

    try:
        builder = PatchBuilder(target, before_path, after_path)
        builder.generate_patch()
        patch_content = builder.build(output_path)
        print(f"Generated grokpatch:\n{patch_content}")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
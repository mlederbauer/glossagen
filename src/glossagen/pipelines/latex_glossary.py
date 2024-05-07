"""Extract glossary from LaTeX document."""

import re
import sys

from glossagen.pipelines.generate_glossary import GlossaryGenerator, ResearchDoc


def extract_text_from_latex(latex_file_path: str) -> str:
    """Extract readable text from .tex document, focusing on content between begin and end doc."""
    text = []
    with open(latex_file_path, encoding="utf-8") as file:
        capture = False
        ignore_block = False
        for line in file:
            if "\\begin{document}" in line:
                capture = True
                continue
            elif "\\end{document}" in line:
                break

            if capture:
                if "\\begin{" in line:
                    # Detect entering a block to ignore
                    ignore_block = True
                if "\\end{" in line:
                    # Detect leaving a block to ignore
                    ignore_block = False
                    continue

                if not ignore_block:
                    # Remove LaTeX commands and comments only if not within an ignored block
                    line_no_comments = re.sub(r"%.*$", "", line)  # Remove comments
                    line_no_cmds = re.sub(
                        r"\\[^\s]*\s*", "", line_no_comments
                    )  # Remove LaTeX commands
                    if line_no_cmds.strip():
                        text.append(line_no_cmds.strip())

    return " ".join(text)


def main(latex_file_path: str) -> None:
    """Extract glossary from LaTeX document."""
    text = extract_text_from_latex(latex_file_path)
    research_doc = ResearchDoc.from_text(text=text, doc_src="LaTeX source")
    glossary_generator = GlossaryGenerator(research_doc)
    glossary = glossary_generator.generate_glossary_from_doc()
    print(glossary)


if __name__ == "__main__":
    latex_path = sys.argv[1] if len(sys.argv) > 1 else "path/to/your/file.tex"
    main(latex_path)

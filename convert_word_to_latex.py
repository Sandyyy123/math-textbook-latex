#!/usr/bin/env python3
"""
convert_word_to_latex.py
Converts a Word (.docx) mathematics textbook manuscript to a LaTeX .tex file
using the math_textbook document class.

Usage:
    python3 convert_word_to_latex.py input.docx grade1_converted.tex --grade 1

Requirements:
    pip install python-docx
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    print("Install python-docx:  pip install python-docx")
    sys.exit(1)


GRADE_COLOR = {1: "blue", 2: "green", 3: "orange"}

PREAMBLE = """\\documentclass{{math_textbook}}
\\gradecolor{{{color}}}

\\begin{{document}}

\\frontmatter
\\title{{\\Huge\\bfseries\\color{{GradeMain}}Mathematics\\\\[6pt]\\large Grade {grade}}}
\\author{{}}
\\date{{}}
\\maketitle
\\tableofcontents

\\mainmatter
"""

FOOTER = """
\\end{document}
"""


def clean_text(text: str) -> str:
    """Escape LaTeX special characters in plain text."""
    replacements = [
        ("&", "\\&"), ("%", "\\%"), ("$", "\\$"),
        ("#", "\\#"), ("_", "\\_"), ("{", "\\{"), ("}", "\\}"),
        ("~", "\\textasciitilde{}"), ("^", "\\textasciicircum{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def detect_style(para) -> str:
    """Map Word paragraph styles to LaTeX environments."""
    style = para.style.name.lower() if para.style else ""
    if "heading 1" in style:
        return "chapter"
    if "heading 2" in style:
        return "section"
    if "heading 3" in style:
        return "subsection"
    if "list" in style or para.text.strip().startswith(("1.", "2.", "a.", "b.")):
        return "listitem"
    return "paragraph"


def has_math(text: str) -> bool:
    """Heuristic: does the paragraph contain mathematical expressions?"""
    return bool(re.search(r"[+\-*/=×÷]|\d+\s*[+\-×÷=]|\bx\b", text))


def convert_paragraph(para, in_exercise_block: bool) -> tuple[str, bool]:
    """Convert one Word paragraph to LaTeX. Returns (latex_str, updated_exercise_flag)."""
    text = para.text.strip()
    if not text:
        return "", in_exercise_block

    ptype = detect_style(para)
    lines = []

    if ptype == "chapter":
        if in_exercise_block:
            lines.append("\\end{practicegrid}\n")
            in_exercise_block = False
        lines.append(f"\n%% ════════════════════════════════════════\n")
        lines.append(f"\\chapter{{{clean_text(text)}}}\n")
        lines.append(f"%% ════════════════════════════════════════\n")

    elif ptype == "section":
        if in_exercise_block:
            lines.append("\\end{practicegrid}\n")
            in_exercise_block = False
        lines.append(f"\n\\section{{{clean_text(text)}}}\n")

    elif ptype == "subsection":
        if in_exercise_block:
            lines.append("\\end{practicegrid}\n")
            in_exercise_block = False
        lines.append(f"\n\\subsection*{{{clean_text(text)}}}\n")

    elif ptype == "listitem":
        if not in_exercise_block:
            lines.append("\\begin{practicegrid}\n")
            in_exercise_block = True
        # Strip leading number/letter prefix
        item_text = re.sub(r"^[\da-z][.)\s]+", "", text, flags=re.IGNORECASE).strip()
        if has_math(item_text):
            lines.append(f"  \\item ${clean_text(item_text)}$ \\blank\n")
        else:
            lines.append(f"  \\item {clean_text(item_text)}\n")

    else:
        if in_exercise_block:
            lines.append("\\end{practicegrid}\n")
            in_exercise_block = False
        # Detect learning objective / worked example / remember heuristics
        lower = text.lower()
        if lower.startswith(("by the end", "students will", "pupils will")):
            lines.append("\\begin{learningobjective}\n")
            lines.append(clean_text(text) + "\n")
            lines.append("\\end{learningobjective}\n")
        elif lower.startswith(("example", "worked example", "let us")):
            lines.append("\\begin{workedexample}\n")
            lines.append(clean_text(text) + "\n")
            lines.append("\\end{workedexample}\n")
        elif lower.startswith(("remember", "note:", "tip:")):
            lines.append("\\begin{remember}\n")
            lines.append(clean_text(text) + "\n")
            lines.append("\\end{remember}\n")
        else:
            lines.append(clean_text(text) + "\\par\n")

    return "".join(lines), in_exercise_block


def convert(docx_path: str, out_path: str, grade: int) -> None:
    doc = Document(docx_path)
    color = GRADE_COLOR.get(grade, "blue")

    out_lines = [PREAMBLE.format(color=color, grade=grade)]
    in_exercise = False

    for para in doc.paragraphs:
        latex_chunk, in_exercise = convert_paragraph(para, in_exercise)
        if latex_chunk:
            out_lines.append(latex_chunk)

    if in_exercise:
        out_lines.append("\\end{practicegrid}\n")

    out_lines.append(FOOTER)

    Path(out_path).write_text("".join(out_lines), encoding="utf-8")
    print(f"Done — written to {out_path}")
    print(f"Compile with:  pdflatex {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert Word textbook manuscript to LaTeX")
    parser.add_argument("input", help="Path to .docx file")
    parser.add_argument("output", help="Output .tex file path")
    parser.add_argument("--grade", type=int, choices=[1, 2, 3], default=1,
                        help="Grade level (determines color theme)")
    args = parser.parse_args()
    convert(args.input, args.output, args.grade)


if __name__ == "__main__":
    main()

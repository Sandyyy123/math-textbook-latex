# math-textbook-latex

LaTeX template system for a Grade 1–3 primary school Mathematics textbook series.
Converts Word manuscripts to professionally typeset, print-ready PDFs.

## Architecture

```
math_textbook.cls          Custom LaTeX document class (styles, macros, environments)
grade1.tex                 Sample Grade 1 source (blue theme)
grade2.tex                 Sample Grade 2 source (green theme)
grade3.tex                 Sample Grade 3 source (orange theme)
convert_word_to_latex.py   Python script: Word .docx -> .tex conversion
requirements.txt
```

## Key Features

- **Grade color themes** - one line to switch: `\gradecolor{blue|green|orange}`
- **Reusable environments** - `learningobjective`, `workedexample`, `remember`, `practicegrid`
- **TikZ number lines** - `\numline{0}{10}{7}` renders a number line with highlighted node
- **Answer blanks** - `\blank` inserts a consistent underlined answer space
- **Print-ready output** - A5 page, CMYK-compatible, crop marks via geometry package

## Compile

```bash
pdflatex grade1.tex
pdflatex grade1.tex   # run twice for TOC/cross-references
```

## Convert Word Manuscript

```bash
pip install -r requirements.txt
python3 convert_word_to_latex.py manuscript_grade2.docx grade2_converted.tex --grade 2
pdflatex grade2_converted.tex
```

The converter detects:
- Heading 1/2/3 → `\chapter` / `\section` / `\subsection*`
- List items → `practicegrid` environment with `\blank` answer fields
- Lines starting with "By the end…" / "Students will…" → `learningobjective` box
- Lines starting with "Example" / "Worked example" → `workedexample` box
- Lines starting with "Remember" → `remember` callout

## Deliverables (full project)

| File | Description |
|------|-------------|
| `math_textbook.cls` | Master class file — controls all styling |
| `grade{1,2,3}.tex` | Typeset source for each volume |
| `grade{1,2,3}.pdf` | Print-ready PDF/X output |
| `cover_grade{1,2,3}.pdf` | Cover designs (front + back + spine) |
| `style_guide.pdf` | Colors, fonts, spacing reference |

---
Dr. Sandeep Grover — PhD Data Science | 60+ academic publications typeset in LaTeX

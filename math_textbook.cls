\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{math_textbook}[2026/05/27 Primary School Mathematics Textbook]

\LoadClass[12pt,a5paper]{book}

%% ── Packages ──────────────────────────────────────────────────────────────────
\RequirePackage[a5paper, top=2cm, bottom=2.2cm, left=2cm, right=2cm]{geometry}
\RequirePackage{xcolor}
\RequirePackage{fontenc}
\RequirePackage{inputenc}
\RequirePackage{amsmath,amssymb}
\RequirePackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc}
\RequirePackage{mdframed}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\RequirePackage{graphicx}
\RequirePackage{setspace}
\RequirePackage{fancyhdr}
\RequirePackage{hyperref}

%% ── Grade colours (set via \gradecolor{blue/green/orange}) ───────────────────
\newcommand{\gradecolor}[1]{%
  \ifstrequal{#1}{blue}  {\colorlet{GradeMain}{blue!70!black}\colorlet{GradePale}{blue!10}}{}%
  \ifstrequal{#1}{green} {\colorlet{GradeMain}{green!60!black}\colorlet{GradePale}{green!10}}{}%
  \ifstrequal{#1}{orange}{\colorlet{GradeMain}{orange!80!black}\colorlet{GradePale}{orange!10}}{}%
}
\gradecolor{blue} % default

%% ── Typography ────────────────────────────────────────────────────────────────
\setstretch{1.4}
\setlength{\parskip}{6pt}
\setlength{\parindent}{0pt}

%% ── Chapter / section styles ─────────────────────────────────────────────────
\titleformat{\chapter}[block]
  {\color{GradeMain}\LARGE\bfseries}
  {\thechapter.}{10pt}{}[{\color{GradeMain}\titlerule[2pt]}]

\titleformat{\section}
  {\color{GradeMain}\large\bfseries}
  {\thesection}{8pt}{}

%% ── Header / footer ──────────────────────────────────────────────────────────
\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE,RO]{\small\color{GradeMain}\rightmark}
\fancyhead[LO,RE]{\small\color{GradeMain}\leftmark}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}

%% ── Learning Objective box ───────────────────────────────────────────────────
\newenvironment{learningobjective}{%
  \begin{mdframed}[backgroundcolor=GradePale, linecolor=GradeMain,
    linewidth=2pt, leftline=true, rightline=false, topline=false, bottomline=false,
    innerleftmargin=10pt, innerrightmargin=10pt, innertopmargin=8pt, innerbottommargin=8pt]
  \textcolor{GradeMain}{\small\bfseries\MakeUppercase{Learning Objective}}\par\smallskip
}{%
  \end{mdframed}
}

%% ── Worked Example box ───────────────────────────────────────────────────────
\newenvironment{workedexample}[1][Example]{%
  \begin{mdframed}[backgroundcolor=yellow!8, linecolor=orange!70!black,
    linewidth=1pt, roundcorner=5pt,
    innerleftmargin=12pt, innerrightmargin=12pt, innertopmargin=10pt, innerbottommargin=10pt]
  \textcolor{orange!80!black}{\bfseries #1}\par\smallskip
}{%
  \end{mdframed}
}

%% ── Remember! callout ────────────────────────────────────────────────────────
\newenvironment{remember}{%
  \begin{mdframed}[backgroundcolor=red!5, linecolor=red!60!black,
    linewidth=1pt, roundcorner=4pt,
    innerleftmargin=10pt, innerrightmargin=10pt, innertopmargin=8pt, innerbottommargin=8pt]
  \textcolor{red!70!black}{\bfseries\small Remember!}\par\smallskip
}{%
  \end{mdframed}
}

%% ── Practice grid (2-column exercise list) ───────────────────────────────────
\newenvironment{practicegrid}{%
  \begin{enumerate}[label=\textbf{\arabic*.}, itemsep=12pt, leftmargin=*, columns=2]
}{%
  \end{enumerate}
}

%% ── Answer blank ─────────────────────────────────────────────────────────────
\newcommand{\blank}{\underline{\hspace{2cm}}}

%% ── Number line (TikZ) ───────────────────────────────────────────────────────
% Usage: \numberline{0}{10}{5}  => line from 0 to 10, highlight node at 5
\newcommand{\numline}[3]{%
  \begin{tikzpicture}[scale=0.7]
    \draw[->, thick, GradeMain] (#1-0.5,0) -- (#2+0.5,0);
    \foreach \x in {#1,...,#2} {
      \draw[thick] (\x, 0.15) -- (\x, -0.15);
      \node[below] at (\x,-0.2) {\small\x};
    }
    \filldraw[GradeMain] (#3,0) circle (4pt);
  \end{tikzpicture}%
}

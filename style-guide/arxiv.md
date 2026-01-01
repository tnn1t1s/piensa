arXiv-Style Typesetting Guide

(Fonts, layout, and PDF production standards)

Goal

Produce a PDF that visually matches a typical arXiv paper:

conservative typography

no decorative fonts

no modern report styling

no layout experimentation

If the output looks “designed,” it is wrong.

Canonical Reference

Target the visual style of:

arXiv PDFs in cs.CL, cs.LG, q-bio, cog sci

Journals like Cognition, Science, PNAS

This means:

LaTeX defaults

Times-like serif body

Minimal spacing

No color, no flair

Fonts (non-negotiable)
Body font

Times / Times New Roman equivalent

In LaTeX: \usepackage{times} or newtxtext

Math font

Default LaTeX math (Computer Modern–style)

Do not mix math font families

Headings

Same serif font as body

No sans-serif headings

Monospace

Only for code blocks

Default LaTeX \texttt{} or Courier

Multilingual / CJK text

If the paper includes Chinese, Hebrew, or other non-Latin scripts:

Required

Use XeLaTeX

Install xeCJK

Explicitly set CJK fonts

Acceptable CJK fonts

Noto Serif CJK

Source Han Serif

Songti / SimSun (acceptable but less ideal)

Example (LaTeX)
\usepackage{xeCJK}
\setCJKmainfont{Noto Serif CJK SC}

Rules

CJK text must render correctly

Missing glyphs are unacceptable

Do not downgrade output to avoid font setup

Page layout
Paper size

US Letter or A4 (either is fine)

Use standard margins

Margins (LaTeX defaults)

~1 inch (2.5 cm)

Columns

Single column (unless journal explicitly requires two)

Section formatting
Section headers

Serif

Bold

Numbered

No color

No horizontal rules

Example:

\section{Methods}
\subsection{Experimental Design}

Paragraphs

Justified

No extra spacing between paragraphs

Standard LaTeX indentation is fine

Tables
Style

Black and white only

Horizontal rules only (top, mid, bottom)

No vertical rules

Font

Same as body

Slightly smaller allowed (\small)

Example (LaTeX convention)
\begin{tabular}{lccc}
\toprule
Adapter & Prompt & Δ & Unclear \\
\midrule
EN & EN & 54\% & 0\% \\
\bottomrule
\end{tabular}

Figures

Black and white preferred

Simple line plots

No shaded backgrounds

Captions below figure

Referenced explicitly in text

Citations & references
In-text

Author–year or numeric (be consistent)

No hyperlinks in body text

References section

Plain text

No hanging design

No DOI badges

No colored links

Pandoc-specific guidance (important)

If using Pandoc → LaTeX → PDF:

DO

Use a minimal LaTeX template

Let LaTeX control layout

Pass font configuration explicitly

DO NOT

Use Pandoc default HTML-inspired templates

Use sans-serif defaults

Use “modern” Pandoc PDF themes

Recommended invocation
pandoc paper.md \
  --pdf-engine=xelatex \
  --template=templates/arxiv.tex \
  -V mainfont="Times New Roman" \
  -V fontsize=10pt \
  -V papersize=letter \
  -o paper.pdf

Anti-patterns (hard stop)

The following indicate non-arXiv style:

Sans-serif body text

Large section spacing

Colored headings

Modern report typography

Wide margins

Excessive whitespace

“Pretty” fonts

Markdown-styled tables in PDF

If you see any of these, the output is wrong.

Agent behavior rules

Agents must follow these rules:

Do not improvise typography

Do not choose fonts

Do not accept degraded output

If a required font/package is missing, ask the user

Prefer LaTeX defaults over customization

One-line heuristic (for agents)

If the PDF would not look out of place on arXiv in 2012, it is probably correct.

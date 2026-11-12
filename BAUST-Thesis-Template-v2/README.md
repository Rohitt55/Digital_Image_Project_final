# BAUST CSE Thesis Template

A LaTeX template for B.Sc. Engineering thesis reports, Department of Computer
Science and Engineering, Bangladesh Army University of Science and Technology
(BAUST).

Every chapter and front-matter section contains short *italicized
instruction text* explaining what should go in that section. Replace this
text with your own writing as you go, and delete the instruction paragraphs
before final submission.

## Quick start: edit your details in ONE place

Open `main.tex` and edit the **THESIS METADATA** block near the top:

```
\newcommand{\thesistitle}{Title of the Thesis}
\newcommand{\studentOneName}{Student Name 1}
\newcommand{\studentOneID}{XXXXXXXXXXXX}
\newcommand{\studentTwoName}{Student Name 2}
\newcommand{\studentTwoID}{XXXXXXXXXXXX}
\newcommand{\supervisorName}{Name of Supervisor}
...
```

These macros are reused automatically on the title page, certificate, board
of examiners, candidate's declaration, running header, and biographies — so
your title and names stay consistent and you never have to edit them in
multiple files.

## How to use

1. **Metadata** — fill in the metadata block in `main.tex` (above).
2. **Board of examiners** — fill in `FrontMatters/board_of_examiners.tex` and
   `board_of_examiners_2nd.tex` with examiner names. Add/remove members as
   needed (duplicate the `\item` blocks and keep numbering consistent across
   both files).
3. **Declaration, acknowledgments, abstract** — fill in the corresponding
   files in `FrontMatters/`.
4. **Chapters** — write your content in `Chapters/1_introduction.tex`
   through `6_conclusionandfutureworks.tex`. Each chapter already has the
   standard section headings used in BAUST CSE theses.
5. **References** — add BibTeX entries to `references.bib` and cite them with
   `\cite{}`. Bibliography style is IEEEtran (see note below).
6. **Appendix** — `BackMatter/appendix_a.tex` is free-form (code listings,
   raw data, etc.). Add more appendices (B, C, ...) by duplicating the
   "Appendix A" block in `main.tex` and creating new files in `BackMatter/`.
7. **Biography** — fill in `BackMatter/biography 1.tex` and `biography 2.tex`.
   Each appears on its own page with a passport-size photo placeholder in the
   top-right corner — replace `Figures/photo_placeholder.png` with each
   student's actual photo (keep roughly 3.5cm x 4.5cm, passport size).

## Figures and tables

- **Figures**: captions appear *below* the figure, auto-numbered as
  "Figure <chapter>.<n>: ..." (e.g. Figure 3.1).
- **Tables**: captions appear *above* the table (research-paper style) and
  use `booktabs` for a clean look. Auto-numbered as "Table <chapter>.<n>".
- **Wide/landscape tables**: use the `sidewaystable` environment (from the
  `rotating` package) — see Table 3.2 in `Chapters/3_methodology.tex`.
- Reference any figure/table in text with `\ref{}` using its `\label{}`.

## Compiling

Use pdfLaTeX + BibTeX:

```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

On Overleaf, set the compiler to pdfLaTeX and click Recompile — it handles
the BibTeX step automatically.

### Bibliography style note

The bibliography uses `\bibliographystyle{IEEEtran}`, which requires the file
`IEEEtran.bst`. This file ships with full TeX Live / MiKTeX installations and
with Overleaf, so no extra file is needed there. If you compile locally and
get "I couldn't open style file IEEEtran.bst", either install the `IEEEtran`
package, or switch the style to the always-bundled equivalent:
`\bibliographystyle{ieeetr}`.

## Notes

- Page numbering: front matter uses lowercase Roman numerals, the main body
  uses Arabic numerals starting from Chapter 1.
- Logo: `Figures/BAUSTlogo.png` is used on the title page. Replace it with
  your own logo if needed (keep the same filename or update the path in
  `FrontMatters/title.tex`).
- `\usepackage{lipsum}` is included only for placeholder text; you can remove
  it once you no longer need dummy paragraphs.

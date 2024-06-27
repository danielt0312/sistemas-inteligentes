rm *.pdf *.aux *.bbl *.blg *.out *.xlm *.nav *.toc *.vrb
pdflatex -interaction nonstopmode -shell-escape -synctex=1 main.tex
bibtex main
pdflatex -interaction nonstopmode -shell-escape -synctex=1 main.tex
pdflatex -interaction nonstopmode -shell-escape -synctex=1 main.tex
rm *.aux *.bbl *.blg *.out *.xlm *.nav *.toc *.vrb
xreader main.pdf


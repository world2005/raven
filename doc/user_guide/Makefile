SRCFILE = raven_user_guide
LATEX_FLAGS=-shell-escape
GUIDE_FILES = raven_user_guide.tex statisticalAnalysis.tex forwardSampling.tex singleRunAndPlot.tex adaptiveSampling.tex dataMining.tex reducedOrderModeling.tex ravenStructure.tex ravenOverview.tex introduction.tex manualStructure.tex manualFormats.tex HowToRun.tex ../version.tex
MAKE_DIR = $(shell pwd)

#all: raven_user_guide.pdf
all: tidy

tidy: $(GUIDE_FILES)
	pdflatex $(LATEX_FLAGS) $(SRCFILE).tex
	bibtex $(SRCFILE)
	pdflatex $(LATEX_FLAGS) $(SRCFILE).tex
	pdflatex $(LATEX_FLAGS) $(SRCFILE).tex

draft: $(GUIDE_FILES)

	pdflatex $(LATEX_FLAGS) "\def\DRAFT{1}\input{$(SRCFILE).tex}"
	bibtex $(SRCFILE)
	pdflatex $(LATEX_FLAGS) "\def\DRAFT{1}\input{$(SRCFILE).tex}"
	pdflatex $(LATEX_FLAGS) "\def\DRAFT{1}\input{$(SRCFILE).tex}"

.PHONY: clean

clean:
	@rm -f *~ *.aux *.bbl *.blg *.log *.out *.toc *.lot *.lof $(SRCFILE).pdf

#Short method of creating version file, offical version is in make_docs.sh script
../version.tex : $(MANUAL_FILES)
	git log -1 --format="%H %an %aD" .. > ../version.tex

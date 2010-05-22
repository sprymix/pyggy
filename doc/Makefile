
# Path to python doc directory
PYTHONDOC= ../../../Python-2.3.4/Doc
ADDRREF= "See the <a href=\"http://www.lava.net/~newsham/pyggy/\">PyGgy Home Page</a>."


PAPER=letter
TEXINPUTS= $(PYTHONDOC)/commontex:

COMMONSTYLES= $(PYTHONDOC)/texinputs/python.sty \
	$(PYTHONDOC)/texinputs/pypaper.sty

INDEXSTYLES= $(PYTHONDOC)/texinputs/python.ist

MANSTYLES= $(PYTHONDOC)/texinputs/fncychap.sty \
	$(PYTHONDOC)/texinputs/manual.cls \
	$(COMMONSTYLES)

COMMONTEX= $(PYTHONDOC)/commontex/copyright.tex \
	$(PYTHONDOC)/commontex/license.tex \
	$(PYTHONDOC)/commontex/patchlevel.tex \
	$(PYTHONDOC)/commontex/boilerplate.tex

DOCFILES= $(MANSTYLES) $(INDESTYLES) \
	pyggy.tex apiref.tex future.tex gramspec.tex intro.tex \
	lexspec.tex quickstart.tex

MKHOWTO=   TEXINPUTS=$(TEXINPUTS) $(PYTHONDOC)/tools/mkhowto
MKDVI=     $(MKHOWTO) --paper=$(PAPER) --dvi
MKHTML=    $(MKHOWTO) --html \
	--iconserver icons --favicon icons/pyfav.gif \
	--address $(ADDRREF) --dvips-safe
	# --about html/stdabout.dat \
	#--up-link index.html \
	#--up-title "Python Documentation Index" \
	#--global-module-index "../modindex.html" --dvips-safe
MKPDF=     $(MKHOWTO) --paper=$(PAPER) --pdf
MKPS=      $(MKHOWTO) --paper=$(PAPER) --ps


# ------------------------------------------------
all: html/pyggy.css html/pyggy.html

html/icons : 
	cp -r $(PYTHONDOC)/html/icons html

html/pyggy.css :
	cp $(PYTHONDOC)/html/style.css $@

html/pyggy.html : $(DOCFILES) html/icons
	$(MKHTML) --dir html pyggy.tex

pyggy.pdf : $(DOCFILES)
	$(MKPDF) pyggy.tex

pyggy.ps : $(DOCFILES)
	$(MKPS) pyggy.tex


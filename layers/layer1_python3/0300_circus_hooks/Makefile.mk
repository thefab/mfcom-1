include ../../../adm/root.mk
include $(MFEXT_HOME)/share/subdir_root.mk

EGG_P3=circus_hooks-0.0.0-py$(PYTHON3_SHORT_VERSION).egg

clean:: pythonclean

all:: dist/$(EGG_P3)

dist/$(EGG_P3):
	python setup.py install --prefix=$(MFCOM_HOME)/opt/python3

test:
	@echo "***** PYTHON3 TESTS *****"
	flake8.sh --exclude=build .
	find . -name "*.py" ! -path './build/*' -print0 |xargs -0 layer_wrapper --layers=python3_circus@mfext -- pylint.sh --errors-only

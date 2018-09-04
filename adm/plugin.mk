NAME:=$(shell config.py config.ini general name)
VERSION:=$(shell config.py config.ini general version |sed "s/{{MODULE_VERSION}}/$${MODULE_VERSION}/g")
RELEASE:=1

ifneq ("$(wildcard python3_virtualenv_sources/requirements-to-freeze.txt)","")
	REQUIREMENTS3:=python3_virtualenv_sources/requirements3.txt
else
	REQUIREMENTS3:=
endif
ifneq ("$(wildcard python3_virtualenv_sources/prerequirements-to-freeze.txt)","")
	REQUIREMENTS3:=python3_virtualenv_sources/prerequirements3.txt $(REQUIREMENTS3)
endif
ifneq ("$(REQUIREMENTS3)","")
	PREREQ:=$(REQUIREMENTS3) python3_virtualenv_sources/src
	DEPLOY:=local/lib/python$(PYTHON3_SHORT_VERSION)/site-packages/requirements3.txt
endif
ifneq ("$(wildcard python2_virtualenv_sources/requirements-to-freeze.txt)","")
	REQUIREMENTS2:=python2_virtualenv_sources/requirements2.txt
else
	REQUIREMENTS2:=
endif
ifneq ("$(wildcard python2_virtualenv_sources/prerequirements-to-freeze.txt)","")
	REQUIREMENTS2:=python2_virtualenv_sources/prerequirements2.txt $(REQUIREMENTS2)
endif
ifneq ("$(REQUIREMENTS2)","")
	PREREQ:=$(REQUIREMENTS2) python2_virtualenv_sources/src
	DEPLOY:=local/lib/python$(PYTHON2_SHORT_VERSION)/site-packages/requirements2.txt
endif
LAYERS=$(shell cat .layerapi2_dependencies |tr '\n' ',' |sed 's/,$$/\n/')

all: $(PREREQ) $(DEPLOY)

clean:
	rm -Rf local *.plugin *.tar.gz python?_virtualenv_sources/*.tmp python?_virtualenv_sources/freezed_requirements.* python?_virtualenv_sources/tempolayer*

superclean: clean
	rm -Rf python?_virtualenv_sources/requirements?.txt python?_virtualenv_sources/prerequirements?.txt python?_virtualenv_sources/src

freeze: superclean $(REQUIREMENTS3) $(REQUIREMENTS2)

local/lib/python$(PYTHON3_SHORT_VERSION)/site-packages/requirements3.txt: $(REQUIREMENTS3) python3_virtualenv_sources/src
	_install_plugin_virtualenv $(NAME) $(VERSION) $(RELEASE)

local/lib/python$(PYTHON2_SHORT_VERSION)/site-packages/requirements2.txt: $(REQUIREMENTS2) python2_virtualenv_sources/src
	_install_plugin_virtualenv $(NAME) $(VERSION) $(RELEASE)

python3_virtualenv_sources/requirements3.txt: python3_virtualenv_sources/requirements-to-freeze.txt
	cd python3_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- freeze_requirements requirements-to-freeze.txt >requirements3.txt

python2_virtualenv_sources/requirements2.txt: python2_virtualenv_sources/requirements-to-freeze.txt
	cd python2_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- freeze_requirements requirements-to-freeze.txt >requirements2.txt

python3_virtualenv_sources/prerequirements3.txt: python3_virtualenv_sources/prerequirements-to-freeze.txt
	cd python3_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- freeze_requirements prerequirements-to-freeze.txt >prerequirements3.txt

python2_virtualenv_sources/prerequirements2.txt: python2_virtualenv_sources/prerequirements-to-freeze.txt
	cd python2_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- freeze_requirements prerequirements-to-freeze.txt >prerequirements2.txt

python3_virtualenv_sources/src: $(REQUIREMENTS3)
	if test -f python3_virtualenv_sources/prerequirements3.txt; then \
	    cd python3_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- download_compile_requirements prerequirements3.txt; \
	fi
	if test -f python3_virtualenv_sources/requirements3.txt; then \
	    cd python3_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- download_compile_requirements requirements3.txt; \
	fi

python2_virtualenv_sources/src: $(REQUIREMENTS2)
	if test -f python2_virtualenv_sources/prerequirements2.txt; then \
	    cd python2_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- download_compile_requirements prerequirements2.txt; \
	fi
	if test -f python2_virtualenv_sources/requirements2.txt; then \
	    cd python2_virtualenv_sources && layer_wrapper --empty --layers=$(LAYERS) -- download_compile_requirements requirements2.txt; \
	fi

release: $(PREREQ) clean
	layer_wrapper --empty --layers=$(LAYERS) -- _plugins.make --show-plugin-path

develop: $(PREREQ) $(DEPLOY)
	_plugins.develop $(NAME)

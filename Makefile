MODULE=MFCOM
MODULE_LOWERCASE=mfcom

-include adm/root.mk
-include $(MFEXT_HOME)/share/main_root.mk

all:: directories
	cd adm && $(MAKE)
	cd config && $(MAKE)
	cd synutil_c && $(MAKE)
	cd layers && $(MAKE)
	cd synutil_lua && $(MAKE)

clean::
	cd synutil_lua && $(MAKE) clean
	cd synutil_c && $(MAKE) clean
	cd config && $(MAKE) clean
	cd adm && $(MAKE) clean
	cd layers && $(MAKE) clean

directories:
	@for DIR in tmp opt/python2/lib/python$(PYTHON2_SHORT_VERSION)/site-packages opt/python3/lib/python$(PYTHON3_SHORT_VERSION)/site-packages; do mkdir -p $(MFCOM_HOME)/$${DIR}; done

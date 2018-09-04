ifeq ($(MODULE),MFCOM)
	CRONTAB_TARGET=
	LOGROTATE_TARGET=
else
	CRONTAB_TARGET=$(MODULE_HOME)/config/crontab
	LOGROTATE_TARGET=$(MODULE_HOME)/config/logrotate.conf
endif

all:: $(MODULE_HOME)/config/version $(CRONTAB_TARGET) $(LOGROTATE_TARGET)

$(MODULE_HOME)/config/telegraf.conf: $(wildcard telegraf.conf.custom) $(MFEXT_HOME)/share/templates/telegraf.conf
	@mkdir -p $(MODULE_HOME)/config
	_make_file_from_template.sh telegraf.conf .custom >$@ || { rm -f $@ ; false ; }

$(MODULE_HOME)/config/circus.ini: $(wildcard circus.ini.custom) $(MFEXT_HOME)/share/templates/circus.ini
	@mkdir -p $(MODULE_HOME)/config
	_make_file_from_template.sh circus.ini .custom >$@ || { rm -f $@ ; false ; }

$(MODULE_HOME)/config/crontab: $(wildcard crontab.custom)
	@mkdir -p $(MODULE_HOME)/config
	$(MFEXT_HOME)/bin/_make_file_from_template.sh crontab .custom >$@ || { rm -f $@ ; false ;}

$(MODULE_HOME)/config/logrotate.conf: $(wildcard logrotate.conf.custom)
	@mkdir -p $(MODULE_HOME)/config
	$(MFEXT_HOME)/bin/_make_file_from_template.sh logrotate.conf .custom >$@ || { rm -f $@ ; false ;}

LIBS=libsynutil.so
INCLUDES=synutil.h
BINS=echo_clean echo_ok echo_nok echo_warning echo_running echo_bold get_unique_hexa_identifier

include ../adm/root.mk
include $(MFEXT_HOME)/share/subdir_root.mk

_LIBS=-L. $(shell pkg-config --libs glib-2.0 gobject-2.0 gthread-2.0)
_INCLUDES=-I. $(shell pkg-config --cflags glib-2.0 gobject-2.0 gthread-2.0)
CC=gcc
DEBUG=no
ifeq ($(DEBUG),yes)
	DEBUG_CFLAGS=-g
endif
CFLAGS=-Wall -fPIC $(DEBUG_CFLAGS) $(COVERAGE_CFLAGS)

OBJECTS=synutil.o

clean::
	rm -f $(OBJECTS) $(BINS) $(LIBS)

synutil.o: synutil.c synutil.h _synutil.h
	$(CC) -c $(CFLAGS) $(_INCLUDES) $<

libsynutil.so: $(OBJECTS)
	$(CC) -shared $(CFLAGS) $(_INCLUDES) $(_LIBS) -o $@ $^

echo_ok: echo_ok.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

get_unique_hexa_identifier: get_unique_hexa_identifier.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

echo_clean: echo_clean.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

echo_warning: echo_warning.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

echo_running: echo_running.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

echo_nok: echo_nok.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

echo_bold: echo_bold.c $(OBJECTS)
	$(CC) -o $@ $(CFLAGS) $(_INCLUDES) $(_LIBS) $^

check: all
	./test_synutil && echo "OK"

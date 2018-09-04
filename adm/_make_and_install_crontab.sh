#!/bin/bash

echo -n "- Building crontab file..."
echo_running
_make_crontab.sh >"${MODULE_RUNTIME_HOME}/tmp/config_auto/crontab" 2>"${MODULE_RUNTIME_HOME}/tmp/crontab_errors.$$"
if test $? -ne 0; then
    echo_nok 
    echo_bold "ERROR: see ${MODULE_RUNTIME_HOME}/tmp/crontab_errors.$$ for details"
    exit 1
fi
if test -s "${MODULE_RUNTIME_HOME}/tmp/crontab_errors.$$"; then
    echo_nok
    echo_bold "ERROR: see ${MODULE_RUNTIME_HOME}/tmp/crontab_errors.$$ for details"
    exit 1
fi

rm -f "${MODULE_RUNTIME_HOME}/tmp/crontab_errors.$$"
echo_ok

echo -n "- Installing crontab file..."
echo_running
deploycron_file "${MODULE_RUNTIME_HOME}/tmp/config_auto/crontab"
if test $? -eq 0; then
    echo_ok
else
    echo_nok
    exit 1
fi

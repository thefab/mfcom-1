#!/bin/bash

set -eu

if ! test -s "${MODULE_HOME}/config/crontab"; then
    exit 0
fi

RUNTIME_SUFFIX=""
if test "${MODULE_RUNTIME_SUFFIX:-}" != ""; then
    RUNTIME_SUFFIX="export MODULE_RUNTIME_SUFFIX=${MODULE_RUNTIME_SUFFIX} ; "
fi
export RUNTIME_SUFFIX

cat "${MODULE_HOME}/config/crontab" |envtpl

if test -d "${MODULE_RUNTIME_HOME}/var/plugins"; then
    for dir in ${MODULE_RUNTIME_HOME}/var/plugins/*; do
        if test -s "${dir}/crontab"; then
            BDIR=$(basename "${dir}")
            echo "##### BEGINNING OF METWORK ${MODULE} PLUGIN ${BDIR} CRONTAB #####"
            cat "${dir}/crontab" | envtpl
            echo "##### END OF METWORK ${MODULE} PLUGIN ${BDIR} CRONTAB #####"
        fi
    done
fi

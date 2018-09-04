#!/bin/bash

echo -n "- Uninstalling module crontab..."
echo_running

RES=0

START_LINE="##### BEGINNING OF METWORK ${MODULE} MODULE CRONTAB #####"
STOP_LINE="##### END OF METWORK ${MODULE} MODULE CRONTAB #####"

undeploycron_between "${START_LINE}" "${STOP_LINE}"

N=$(crontab -l 2>/dev/null |grep "${START_LINE}" |wc -l)
if test ${N} -gt 0; then
    echo_nok || RES=1
else
    echo_ok
fi


PLUGINS=$(crontab -l |grep "##### BEGINNING OF METWORK ${MODULE} PLUGIN" |awk '{print $7;}')
for PLUGIN in ${PLUGINS}; do
    echo -n "- Uninstalling plugin ${PLUGIN} crontab..."
    echo_running
    START_LINE="##### BEGINNING OF METWORK ${MODULE} PLUGIN ${PLUGIN} CRONTAB #####"
    STOP_LINE="##### END OF METWORK ${MODULE} PLUGIN ${PLUGIN} CRONTAB #####"
    undeploycron_between "${START_LINE}" "${STOP_LINE}"
    N=$(crontab -l 2>/dev/null |grep "${START_LINE}" |wc -l)
    if test ${N} -gt 0; then
        echo_nok || RES=1
    else
        echo_ok
    fi
done

exit ${RES}

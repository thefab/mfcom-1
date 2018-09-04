#!/bin/bash

WATCHER=$1

echo -n "- Waiting for stop of ${WATCHER}..."
echo_running

I=0
while test ${I} -lt 400; do
    # yes we schedule another time because sometimes circus returns a concurrency error
    _circus_schedule_stop_watcher.sh "${WATCHER}" >/dev/null 2>&1
    circus_status_watcher.sh "${WATCHER}" >/dev/null 2>&1
    if test $? -ne 0; then
        break
    fi
    I=$(expr ${I} + 1)
    sleep 1
done

if test "${I}" -ge 400; then
    echo_nok
    exit 1
else
    echo_ok
    exit 0
fi

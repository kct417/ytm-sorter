#!/bin/bash

SCRIPT_DIR=~/ytm
VENV_PY="$SCRIPT_DIR/.venv/bin/python"
SCRIPT="$SCRIPT_DIR/main.py"

CRON_TIME="0 12 * * *"
CRON_JOB="cd $SCRIPT_DIR && $VENV_PY $SCRIPT" 
CRON_LOG="$SCRIPT_DIR/cron.log"
CRON_LINE="$CRON_TIME $CRON_JOB >> $CRON_LOG 2>&1"
echo "$CRON_LINE"
if ! crontab -l 2>/dev/null | grep -Fxq "$CRON_LINE"; then
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
	echo "Cron job installed:"
	echo "$CRON_LINE"
fi


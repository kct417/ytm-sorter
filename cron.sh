#!/bin/bash

SCRIPT_DIR="/home/ubuntu/ytm"
VENV_PY="$SCRIPT_DIR/.venv/bin/python"
SCRIPT="$SCRIPT_DIR/main.py"
LOG="$SCRIPT_DIR/cron.log"

CRON_SCHEDULE="0 12 * * *"
CRON_LINE="$CRON_SCHEDULE cd $SCRIPT_DIR && $VENV_PY $SCRIPT >> $LOG 2>&1"

# Removes any old line that references script (to avoid duplicates)
(crontab -l 2>/dev/null | grep -Fv "$SCRIPT"; echo "$CRON_LINE") | crontab -

echo "Cron job installed:"
echo "$CRON_LINE"


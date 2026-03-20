DIR=~/ytm-sorter
VENV=~/ytm-sorter/.venv/bin/python
SCRIPT=~/ytm-sorter/main.py

JOB="cd $DIR && $VENV $SCRIPT"
LOG=~/.config/cron/cron.log
CRON="0 12 * * * $JOB >> $LOG 2>&1"
if ! crontab -l 2>/dev/null | grep -Fxq "$CRON"; then
	(
		crontab -l 2>/dev/null
		echo "$CRON"
	) | crontab -
	echo "Cron job installed: $CRON"
fi

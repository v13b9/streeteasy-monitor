#!/bin/bash
CRON_FILE="cron.dat"

if crontab -l; then
    echo "Cron job found, saving to $CRON_FILE..."
    crontab -l > "$CRON_FILE"
    echo "Removing existing cron job..."
    crontab -r
    echo "Cron job stopped and saved to $CRON_FILE."
else
    echo "No cron jobs running."
fi
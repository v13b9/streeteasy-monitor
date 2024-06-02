#!/bin/bash
CRON_FILE="cron.dat"

if [ ! -s "$CRON_FILE" ]; then
    echo "Cron.dat is empty. Write cron job to file or run create_cron.sh"
    exit 1
fi

start_cron_job() {
    echo "Starting cron job:"
    cat "$CRON_FILE"
    crontab "$CRON_FILE"
}

if crontab -l; then
    read -n 1 -p "Cron job already running. Overwrite? (y/n) " ANSWER
    echo
    if [[ "$ANSWER" =~ ^[Yy]$ ]]; then
        echo "Overwriting crontab"
        start_cron_job
    else
        echo "Exiting without overwriting"
    fi
else
    start_cron_job
fi
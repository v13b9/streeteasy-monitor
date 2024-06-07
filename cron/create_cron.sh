#!/bin/bash
# initialize cron and log files
CRON_FILE="cron.dat"
LOG_FILE="cron.log"

# find and set absolute paths
PYTHON_PATH="$(which python)"
PARENT_DIR="$(dirname "$PWD")"
SCRIPT_PATH="$PARENT_DIR/main.py"
LOG_PATH="$PWD/$LOG_FILE"

# set schedule
CRON_SCHEDULE="*/6 * * * *"

write_cron_job() {
    echo "$CRON_SCHEDULE $PYTHON_PATH $SCRIPT_PATH >> $LOG_PATH 2>&1" > "$CRON_FILE"
}

# write cron job to cron.dat
if [ -s "$CRON_FILE" ]; then
    read -n 1 -p "Cron.dat already exists. Overwrite? (y/n) " answer
    echo
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo "Overwriting $CRON_FILE"
        write_cron_job
        exit 0
    else
        echo "Exiting without overwriting"
        exit 0
    fi
else
    echo "Writing $CRON_FILE"
    write_cron_job
    exit 0
fi

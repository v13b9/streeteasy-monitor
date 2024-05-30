#!/bin/bash

# create log file if it doesn't already exist
if [ ! -f cron.dat ]; then
    eval touch cron.dat
fi

# find and set absolute paths
python_path=$(eval which python)
script_path=$(find $PWD -name main.py)
log_path=$(find $PWD -name *.log)

# set schedule
cron_schedule="*/8 * * * *"

# write cron job to cron.dat
if [ -s cron.dat ]; then
    read -n 1 -p "Cron.dat already exists. Overwrite? (y/n) " answer
    echo
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo "Overwriting cron.dat"
        echo "$cron_schedule" $python_path $script_path > cron.dat ">>" $log_path "2>&1"
        exit 0
    else
        echo "Exiting without overwriting"
        exit 0
    fi
else
    echo "Writing cron.dat"
    echo "$cron_schedule" $python_path $script_path > cron.dat ">>" $log_path "2>&1"
    exit 0
fi

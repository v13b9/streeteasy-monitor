#!/bin/bash
if [ ! -s cron.dat ]; then
    echo "Cron.dat is empty. Write cron job to file or run create_cron.sh"
    exit 1
fi

if crontab -l; then
    read -n 1 -p "Cron job already running. Overwrite? (y/n) " answer
    echo
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        echo "Overwriting crontab"
        echo "Starting cron job:"
        cat cron.dat
        crontab < cron.dat
        exit 0
    else
        echo "Exiting without overwriting"
        exit 0
    fi
else
    echo "Starting cron job:"
    cat cron.dat
    crontab < cron.dat
    exit 0
fi
#!/bin/bash
if crontab -l; then
    # save existing cron job to cron.dat
    echo "Stopping cron job"
    crontab -l > cron.dat
    crontab -r
else
    echo "No cron jobs running"
fi
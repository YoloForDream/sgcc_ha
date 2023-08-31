#!/bin/bash

CONFIG_PATH=/data/options.json

if [ ! $PHONE_NUMBER ] && [ -f $CONFIG_PATH ]; then
    PHONE_NUMBER=$(jq --raw-output '.phoneNumber' $CONFIG_PATH)
fi

if [ ! $PHONE_NUMBER ] || [ null == $PHONE_NUMBER ]; then
    echo "error! phoneNumber is null"
    exit 1
fi

if [ ! $PASSWORD ] && [ -f $CONFIG_PATH ];then
    PASSWORD=$(jq --raw-output '.password' $CONFIG_PATH)
fi

if [ ! $PASSWORD ] || [ null == $PASSWORD ]; then
    echo "error! password is null"
    exit 1
fi

if [ ! $HASS_URL ] && [ -f $CONFIG_PATH ]; then
    HASS_URL=$(jq --raw-output '.hass_url' $CONFIG_PATH)
fi

if [ ! $HASS_TOKEN ] && [ -f $CONFIG_PATH ]; then
    HASS_TOKEN=$(jq --raw-output '.hass_token' $CONFIG_PATH)
fi

if [ ! $JOB_START_TIME ] && [ -f $CONFIG_PATH ]; then
    JOB_START_TIME=$(jq --raw-output '.job_start_time' $CONFIG_PATH)
fi

if [ ! $LOG_LEVEL ] && [ -f $CONFIG_PATH ]; then
    LOG_LEVEL=$(jq --raw-output '.logLevel' $CONFIG_PATH)
fi

if [ ! $LOG_LEVEL ] || [ null == $LOG_LEVEL ];then
    LOG_LEVEL=INFO
fi

python3 ./main.py --PHONE_NUMBER=$PHONE_NUMBER --PASSWORD=$PASSWORD --HASS_URL=$HASS_URL --HASS_TOKEN=$HASS_TOKEN --JOB_START_TIME=$JOB_START_TIME --LOG_LEVEL=$LOG_LEVEL

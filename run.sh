#!/bin/bash

CONFIG_PATH=/data/options.json
PHONE_NUMBER="$(bashio::config 'phoneNumber')"
PASSWORD="$(bashio::config 'password')"
HASS_URL="$(bashio::config 'hass_url')"
HASS_TOKEN="$(bashio::config 'hass_token')"
JOB_START_TIME="$(bashio::config 'job_start_time')"
LOG_LEVEL="$(bashio::config 'logLevel')"

python3 ./main.py --PHONE_NUMBER=$PHONE_NUMBER --PASSWORD=$PASSWORD --HASS_URL=$HASS_URL --HASS_TOKEN=$HASS_TOKEN --JOB_START_TIME=$JOB_START_TIME --LOG_LEVEL=$LOG_LEVEL

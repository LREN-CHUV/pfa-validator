#!/bin/bash

docker run \
    --env PFA_PATH="model.txt" \
    --env FEATURES_DB_HOST=db \
    --env FEATURES_DB_PORT=5432 \
    --env FEATURES_DB_NAME=sample \
    --env FEATURES_DB_USER=sample \
    --env FEATURES_DB_PASSWORD=featurespwd \
    --env FEATURES_DB_TABLE=features \
    hbpmip/pfa-validator:0.10.1-2

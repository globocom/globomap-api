#!/bin/bash
if [ -z "${GMAP_DB_PORT}" ]; then
    echo "Environment variable GMAP_DB_PORT is not defined."
    echo "Setting default ..."
    GMAP_DB_PORT=7001
fi

if [ -z "${GMAP_API_PORT}" ]; then
    echo "Environment variable GMAP_API_PORT is not defined."
    echo "Setting default ..."
    GMAP_API_PORT=7002
fi

if [ -z "${GMAP_API_DEBUG_PORT}" ]; then
    echo "Environment variable GMAP_API_DEBUG_PORT is not defined."
    echo "Setting default ..."
    GMAP_API_DEBUG_PORT=7003
fi

if [ -z "${GMAP_KS_ADM_PORT}" ]; then
    echo "Environment variable GMAP_KS_ADM_PORT is not defined."
    echo "Setting default ..."
    GMAP_KS_ADM_PORT=7004
fi

if [ -z "${GMAP_KS_PORT}" ]; then
    echo "Environment variable GMAP_KS_PORT is not defined."
    echo "Setting default ..."
    GMAP_KS_PORT=7005
fi

if [ -z "${GMAP_REDIS_PORT}" ]; then
    echo "Environment variable GMAP_REDIS_PORT is not defined."
    echo "Setting default ..."
    GMAP_REDIS_PORT=7006
fi

echo "GMAP_DB_PORT=$GMAP_DB_PORT" > .env
echo "GMAP_API_PORT=$GMAP_API_PORT" >> .env
echo "GMAP_API_DEBUG_PORT=$GMAP_API_DEBUG_PORT" >> .env
echo "GMAP_KS_ADM_PORT=$GMAP_KS_ADM_PORT" >> .env
echo "GMAP_KS_PORT=$GMAP_KS_PORT" >> .env
echo "GMAP_REDIS_PORT=$GMAP_REDIS_PORT" >> .env

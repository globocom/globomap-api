#!/bin/bash
# Check keystone service
INTERVAL=5
MAX_ATTEMPTS=30
CHECK_COMMAND="curl -sL -w "%{http_code}" http://globomap_keystone:5000 -o /dev/null"
ATTEMPTS=1
HTTP_RET_CODE=`${CHECK_COMMAND}`
while [ "000" = "${HTTP_RET_CODE}" ] && [ ${ATTEMPTS} -le ${MAX_ATTEMPTS} ]; do
    echo "Error connecting to keystone. Attempt ${ATTEMPTS}. Retrying in ${INTERVAL} seconds ..."
    sleep ${INTERVAL}
    ATTEMPTS=$((ATTEMPTS+1))
    HTTP_RET_CODE=`${CHECK_COMMAND}`
done

if [ "000" = "${HTTP_RET_CODE}" ]; then
        echo "Error connecting to keystone. Aborting ..."
        exit 2
fi


./scripts/docker/api/meta_collections.sh
make run

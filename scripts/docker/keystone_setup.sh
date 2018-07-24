#!/bin/bash
while : ; do
    project=$(docker ps | grep globomap_keystone)
    if [[ ! -z "$project" ]]; then
        break;
    else
        sleep 1;
    fi
done
docker exec -it globomap_keystone "/home/keystone.sh"
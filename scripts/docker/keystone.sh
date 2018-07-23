#!/bin/bash
# Check keystone service
INTERVAL=5
MAX_ATTEMPTS=10
CHECK_COMMAND="curl -sL -w "%{http_code}" http://0.0.0.0:35357 -o /dev/null"
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

cd /root
source openrc

token_issue()
{
    echo "Testing list token issue"
    user_id=$(openstack token issue | grep user_id)
    if [[ -z "$user_id" ]]; then
        sleep 2
        token_issue
    fi
}
project_list()
{
    echo "Testing list projects"
    project=$(openstack project list | grep admin)
    if [[ -z "$project" ]]; then
        sleep 2
        project_list
    fi
}
user_list()
{
    echo "Testing list users"
    user=$(openstack user list | grep admin)
    if [[ -z "$user" ]]; then
        sleep 2
        user_list
    fi
}
token_issue
project_list
user_list

## Creating Project
while : ; do
    echo "Creating project GloboMap"
    project=$(openstack project list | grep Globomap)
    if [[ ! -z "$project" ]]; then
        echo "Project created"
        break
    else
        openstack project create --domain default  --description "GloboMap" Globomap
        sleep 1
    fi
done

## Creating Users
create_user()
{   
    user=$1
    echo "User $user"
    while : ; do
        echo "Searching user $user"
        user_match=$(openstack user list | grep $user)
        if [[ ! -z "$user_match" ]]; then
            echo "User created"
            break
        else
            echo "Creating user $user"
            openstack user create --domain default  $user --password $user
            sleep 1
        fi
    done
}

create_user u_globomap_api

## Creating Roles
create_role()
{   
    role=$1
    echo "Role $role"
    while : ; do
        echo "Searching role $role"
        role_match=$(openstack role list | grep $role)
        if [[ ! -z "$role_match" ]]; then
            echo "Role created"
            break
        else
            echo "Creating role $role"
            openstack role create $role
            sleep 1
        fi
    done
}

create_role globomap_admin
create_role globomap_read
create_role globomap_write
create_role globomap_collection
create_role globomap_edge
create_role globomap_graph
create_role globomap_loader_update

## Associating Roles
create_assoc_role()
{   
    user=$1
    role=$2
    while : ; do
        echo "Searching user $user with role $role"
        role_match=$(openstack role assignment list --user $user --names | grep $role)
        if [[ ! -z "$role_match" ]]; then
            echo "Role associated"
            break
        else
            echo "Associating role $role with user $user"
            openstack role add --project Globomap --user $user $role
            sleep 1
        fi
    done
}
create_assoc_role u_globomap_api admin
create_assoc_role u_globomap_api globomap_admin
create_assoc_role u_globomap_api globomap_read
create_assoc_role u_globomap_api globomap_write
create_assoc_role u_globomap_api globomap_collection
create_assoc_role u_globomap_api globomap_edge
create_assoc_role u_globomap_api globomap_graph
create_assoc_role u_globomap_api globomap_loader_update

#!/bin/bash
cd /root
source openrc
echo "create project GloboMap"
openstack project create --domain default  --description "GloboMap" Globomap
sleep 5

echo "create user u_globomap_api"
openstack user create --domain default  u_globomap_api --password u_globomap_api
sleep 5

#openstack service create --name Globomap --description "GloboMap" mapping

echo "create role globomap_admin"
openstack role create globomap_admin
sleep 5
echo "create role globomap_read"
openstack role create globomap_read
sleep 5
echo "create role globomap_write"
openstack role create globomap_write
sleep 5
echo "create role globomap_collection"
openstack role create globomap_collection
sleep 5
echo "create role globomap_edge"
openstack role create globomap_edge
sleep 5
echo "create role globomap_graph"
openstack role create globomap_graph
sleep 5
echo "create role globomap_loader_update"
openstack role create globomap_loader_update
sleep 5

echo "assoc role admin"
openstack role add --project Globomap --user u_globomap_api admin
sleep 5
echo "assoc role globomap_admin"
openstack role add --project Globomap --user u_globomap_api globomap_admin
sleep 5
echo "assoc role globomap_read"
openstack role add --project Globomap --user u_globomap_api globomap_read
sleep 5
echo "assoc role globomap_write"
openstack role add --project Globomap --user u_globomap_api globomap_write
sleep 5
echo "assoc role globomap_collection"
openstack role add --project Globomap --user u_globomap_api globomap_collection
sleep 5
echo "assoc role globomap_edge"
openstack role add --project Globomap --user u_globomap_api globomap_edge
sleep 5
echo "assoc role globomap_graph"
openstack role add --project Globomap --user u_globomap_api globomap_graph
sleep 5
echo "assoc role globomap_loader_update"
openstack role add --project Globomap --user u_globomap_api globomap_loader_update

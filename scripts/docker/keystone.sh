#!/bin/bash
cd /root
source openrc
openstack project create --domain default  --description "GloboMap" Globomap

openstack user create --domain default  u_globomap_api --password u_globomap_api

#openstack service create --name Globomap --description "GloboMap" mapping

openstack role create globomap_admin
openstack role create globomap_read
openstack role create globomap_write
openstack role create globomap_collection
openstack role create globomap_edge
openstack role create globomap_graph
openstack role create globomap_loader_update

openstack role add --project Globomap --user u_globomap_api admin
openstack role add --project Globomap --user u_globomap_api globomap_admin
openstack role add --project Globomap --user u_globomap_api globomap_read
openstack role add --project Globomap --user u_globomap_api globomap_write
openstack role add --project Globomap --user u_globomap_api globomap_collection
openstack role add --project Globomap --user u_globomap_api globomap_edge
openstack role add --project Globomap --user u_globomap_api globomap_graph
openstack role add --project Globomap --user u_globomap_api globomap_loader_update

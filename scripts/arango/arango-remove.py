import sys
import json
import os

from arango import ArangoClient


def main():
    conn = ArangoClient(
        protocol=os.getenv('ARANGO_PROTOCOL', 'http'),
        host=os.getenv('ARANGO_HOST', 'arangodb.globomap.dev.globoi.com'),
        port=os.getenv('ARANGO_PORT', '8529')
    )

    database = conn.db(
        os.getenv('ARANGO_DB', 'globomap'),
        username=os.getenv('ARANGO_USERNAME', 'gmap'),
        password=os.getenv('ARANGO_PASSWORD', 'Adm4gmap')
    )

    graphs = [
        "foreman",
        "keystone",
        "acl",
        "dns",
        "swift",
        "cloud_stack",
        "database",
        "domain",
        "custeio",
        "networking_topology",
        "permission",
        "load_balancing",
        "galeb",
        "zabbix",
        "faas",
        "tsuru",
        "accounts"
    ]

    for graph in graphs:
        try:
            database.delete_graph(name=graph)
        except Exception as err:
            print("delete graph '{}' error. Error: {}".format(graph, err))
        else:
            print("delete graph '{}' ok...".format(graph))

    edges = [
        "foreman_host_dns",
        "custeio_business_service_comp_unit",
        "filer_volume",
        "custeio_process_storage",
        "database_tsuru_service_instance",
        "custeio_process_comp_unit",
        "custeio_client_storage",
        "galeb_target",
        "volume_export",
        "custeio_sub_component_comp_unit",
        "custeio_business_service_component",
        "access",
        "custeio_process_business_service",
        "environment_vlan",
        "pool_comp_unit",
        "custeio_component_sub_component",
        "internet_access",
        "swift_account_tsuru_service_instance",
        "tsuru_pool_comp_unit",
        "custeio_product_storage",
        "vlan_network",
        "team_access",
        "father_environment",
        "galeb_virtual_host_rule",
        "tsuru_service_service_instance",
        "network_comp_unit",
        "custeio_component_storage",
        "galeb_rule_pool",
        "galeb_environment_virtual_host",
        "galeb_environment_vip",
        "galeb_host_environment",
        "export_snapshot",
        "tsuru_pool_app",
        "zone_region",
        "ks_role",
        "custeio_client_comp_unit",
        "custeio_sub_component_storage",
        "zabbix_link",
        "zone_host",
        "host_comp_unit",
        "tsuru_app_service_instance",
        "dns_link",
        "foreman_host_puppet_class",
        "swift_account_ks_project",
        "ldap_group_user",
        "port",
        "custeio_component_comp_unit",
        "dns_domain",
        "custeio_business_service_storage",
        "database_dns",
        "custeio_product_comp_unit",
        "comp_unit_database",
        "bs_user_ldap_user"
    ]

    for edge in edges:
        try:
            database.delete_collection(name=edge)
        except Exception as err:
            print("delete edge '{}' error. Error: {}".format(edge, err))
        else:
            print("delete edge '{}' ok...".format(edge))

    collections = [
        "unknown",
        "volume",
        "foreman_host",
        "tsuru_pool",
        "comp_unit",
        "region",
        "ks_user",
        "zone",
        "zabbix_graph",
        "tag_firewall",
        "swift_account",
        "custeio_process",
        "network",
        "ldap_user",
        "tsuru_app",
        "tsuru_service_instance",
        "dns",
        "database",
        "galeb_pool",
        "galeb_virtual_host",
        "galeb_environment",
        "export",
        "tsuru_service",
        "ks_project",
        "ldap_group",
        "custeio_resource",
        "foreman_puppet_class",
        "vlan",
        "custeio_product",
        "custeio_component",
        "environment",
        "snapshot",
        "vip",
        "pool",
        "galeb_rule",
        "custeio_business_service",
        "custeio_client",
        "custeio_team",
        "custeio_sub_component",
        "domain",
        "internal_metadata",
        "meta_collection",
        "meta_graph",
        "meta_query",
        "bs_user"
    ]

    for collection in collections:
        try:
            database.delete_collection(name=collection)
        except Exception as err:
            print("delete collection '{}' error. Error: {}".format(collection, err))
        else:
            print("delete collection '{}' ok...".format(collection))

if __name__== "__main__":
  main()

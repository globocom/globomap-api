# Globo Map API

Application responsible for reading and writing in ARANGODB. This application has a RESTFul API.

## Starting Project:

` make containers_build ` (Build images.) <br>
` make containers_start ` (Up containers) <br>

## Running local with docker:

` make containers_build ` (When project not started yet.) <br>
` make containers_start ` (When project not started yet.) <br>
` make create_meta_collections ` (Create meta collections in ArangoDB) <br>
` make keystone_config ` (Create roles in Keystone) <br>

## Running Tests:

` make containers_build ` (When project not started yet.) <br>
` make containers_start ` (When project not started yet.) <br>
` make tests `

## Plugin environment variables configuration

All of the environment variables below must be set for the api to work properly.

| Variable                           |  Description                                                                | Example                    |
|------------------------------------|-----------------------------------------------------------------------------|----------------------------|
| ARANGO_DB                          | Database name                                                               | globomap                   |
| ARANGO_USERNAME                    | Database user                                                               | user                       |
| ARANGO_PASSWORD                    | Database password                                                           | password                   |
| ARANGO_PROTOCOL                    | Database protocol                                                           | https                      |
| ARANGO_PORT                        | Database port                                                               | 8529                       |
| ARANGO_HOST                        | Database host                                                               | arangodb.domain.com        |
| VARIABLES of globomap-auth-manager | [globomap-auth-manager](https://github.com/globocom/globomap-auth-manager)  | --                         |

Environment variables needed for the Zabbix plugin to work properly

| Variable                    |  Description            | Example                    |
|-----------------------------|-------------------------|----------------------------|
| ZABBIX_API_URL              | Zabbix API endpoint     | https://ro.api.zabbix.com  |
| ZABBIX_API_USER             | Zabbix username         | username                   |
| ZABBIX_API_PASSWORD         | Zabbix password         | xyz                        |
| ZABBIX_UI_URL               | Zabbix endpoint         | https://zabbix.com         |


### Environment variables configuration from external libs
All of the environment variables below must be set for the application to work properly.

[globomap-auth-manager](https://github.com/globocom/globomap-auth-manager)

### Requirements:
#### Collections in ArangoDB:
meta_collection <br>
meta_graph <br>
meta_query <br>

#### Roles in Keystone:
globomap_admin <br>
globomap_read <br>
globomap_write <br>
globomap_collection <br>
globomap_edge <br>
globomap_graph <br>

#### Using makefile
To create meta collections in ArangoDB<br>
`make create_meta_collections`

To create roles in Keystone<br>
`make keystone_config`

## Licensing

Globo Map API is under [Apache 2 License](./LICENSE)

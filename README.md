# Globo Map API

Application responsible for reading and writing in ARANGODB. This application has a RESTFul API.

## Starting Project:

` make docker `

## Running Tests:

` make docker ` (When project not started yet.)<br>
` make tests `

## Plugin environment variables configuration

All of the environment variables below must be set for the api to work properly.

| Variable                    |  Description            | Example                    |
|-----------------------------|-------------------------|----------------------------|
| ARANGO_DB                   | Database name           | globomap                   |
| ARANGO_USERNAME             | Database user           | user                       |
| ARANGO_PASSWORD             | Database password       | password                   |
| ARANGO_PROTOCOL             | Database protocol       | https                      |
| ARANGO_PORT                 | Database port           | 8529                       |
| ARANGO_HOST                 | Database host           | arangodb.domain.com        |

Environment variables needed for the Zabbix plugin to work properly

| Variable                    |  Description            | Example                    |
|-----------------------------|-------------------------|----------------------------|
| ZABBIX_API_URL              | Zabbix API endpoint     | https://ro.api.zabbix.com  |
| ZABBIX_API_USER             | Zabbix username         | username                   |
| ZABBIX_API_PASSWORD         | Zabbix password         | xyz                        |
| ZABBIX_UI_URL               | Zabbix endpoint         | https://zabbix.com         |

## Licensing

Globo Map API is under [Apache 2 License](./LICENSE)

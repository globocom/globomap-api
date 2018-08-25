# Permissions

### Data Struct
| ACTION | ROLES |
| ------ | ------ |
| **Create Collection** | *globomap_write* --- *globomap_collection* --- *globomap_admin* |
| **Create Edge** | *globomap_write* --- *globomap_edge* --- *globomap_admin* |
| **Create Graph** | *globomap_write* --- *globomap_graph* --- *globomap_admin* |

### Collection Document
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* --- *globomap_collection* |
| **Change** | *globomap_write* --- *globomap_collection* |
| **Delete** | *globomap_write* --- *globomap_collection* |
| **Read** | *globomap_read* --- *globomap_collection* |
| **Search** | *globomap_read* --- *globomap_collection* |

### Edge Document
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* --- *globomap_edge* |
| **Change** | *globomap_write* --- *globomap_edge* |
| **Delete** | *globomap_write* --- *globomap_edge* |
| **Read** | *globomap_read* --- *globomap_edge* |
| **Search** | *globomap_read* --- *globomap_edge* |

### Queries
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* --- *globomap_collection* |
| **Read** | *globomap_read* --- *globomap_collection* |
| **Search** | *globomap_read* --- *globomap_collection* |
| **Execute** | *globomap_read* --- *globomap_collection* |

### Graphs
| ACTION | ROLES |
| ------ | ------ |
| **Read** | *globomap_read* --- *globomap_graph* |
| **Search** | *globomap_read* --- *globomap_graph* |


* Documentar as roles para cada rota


Ter um usuario no keystone:

  http://vault.globoi.com



Criar usuario no keystone
Dar roles necessarias ao serviço Globomap ao usuario


As rotas são autenticadas, precisam de um token
Para conseguir
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "username": "u_globomap_driver_aclapi",
   "password": "u_globomap_driver_aclapi"  
 }' 'https://api.loader.globomap.dev.globoi.com/v2/auth/'

 Mais informações:
  swagger DOC
  https://http://api.loader.globomap.dev.globoi.com/v2
  https://http://api.loader.globomap.globoi.com//v2

As APIs do Globomap usam autenticação por meio do keystone. Mas para o usuário fica transparente.
O vault é uma interface gerencia o keystone da globo. O time storm é o responsavel.
Pedir um usuário no keystone para o time storm:
  informações para o time:
    Cria via vault:
        Cria um usuario aqui http://vault.dev.globoi.com/admin/identity/users
            o usuario precisa ter permissão ao projeto Globomap
        Vai no projeto globomap http://vault.dev.globoi.com/admin/identity/projects/
            E associa ao usuario criado as permissões necessarias

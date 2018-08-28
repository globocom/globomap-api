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

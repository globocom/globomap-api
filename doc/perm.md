# Permissions

### List of Roles
| ROLES | Description |
| ------ | ------ |
| globomap_admin | Administrative Permission |
| globomap_write | Write Permission |
| globomap_read | Read Permission |

### Data Struct
| ACTION | ROLES |
| ------ | ------ |
| **Create Collection** | *globomap_admin* |
| **Create Edge** | *globomap_admin* |
| **Create Graph** | *globomap_admin* |

### Collection Document
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* |
| **Change** | *globomap_write* |
| **Delete** | *globomap_write* |
| **Read** | *globomap_read* |
| **Search** | *globomap_read* |

### Edge Document
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* |
| **Change** | *globomap_write* |
| **Delete** | *globomap_write* |
| **Read** | *globomap_read* |
| **Search** | *globomap_read* |

### Queries
| ACTION | ROLES |
| ------ | ------ |
| **Create** | *globomap_write* |
| **Read** | *globomap_read* |
| **Search** | *globomap_read* |
| **Execute** | *globomap_read* |

### Graphs
| ACTION | ROLES |
| ------ | ------ |
| **Read** | *globomap_read* |
| **Search** | *globomap_read* |

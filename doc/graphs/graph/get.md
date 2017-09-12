# Search Graph by Traversal

----
  Returns json data with list of graphs in DB.

* **URL**

  /v1/graphs/<graph>/traversal

* **Method:**

  `GET`
  
* **URL Params**
  
  Required:
  
  start_vertex=[string]
  
  Optional:
  
  direction=[string] -- outbound | inbound | any -- default: outbound
  item_ordem=[string] -- forward | backward -- default: forward
  strategy=[string] - dfs | bfs -- default: bfs
  order=[string] - preorder | postorder | preorder-expander -- default: None
  edge_uniqueness=[string] - global | path -- default: None
  vertex_uniqueness=[string] - global | path -- default: None
  max_iter=[integer]
  min_depth=[integer]
  max_depth=[integer]

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"edges":[{"_from":"coll1/xxx_1","_id":"edge1/xxx_1","_key":"xxx_1","_rev":"_VldIjxC---","_to":"coll1/xxx_2","id":"1","metadata":null,"name":"yyy","properties":{"key":"value"},"provider":"xxx","timestamp":1501543772}],"graph":"abc","nodes":[{"_id":"coll1/xxx_1","_key":"xxx_1","_rev":"_Vlc2PCO---","id":"1","metadata":null,"name":"yyy","properties":{"key":"value"},"provider":"xxx","timestamp":1501543772},{"_id":"coll1/xxx_2","_key":"xxx_2","_rev":"_VldGaxu---","id":"2","metadata":null,"name":"yyy","properties":{"key":"value"},"provider":"xxx","timestamp":1501543772}]}]`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/graphs/abc/traversal?start_vertex=coll1/xxx_1
  ```

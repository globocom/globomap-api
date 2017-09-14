# List Graphs

----
  Returns json data with list of graphs in DB.

* **URL**

  /v1/graphs

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200
  * **Content:** `[{"links":[{"edge":"edge1","from_collections":["coll1"],"to_collections":["coll2"]},{"edge":"edge2","from_collections":["coll2"],"to_collections":["coll3"]}],"name":"graph1"}]`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/graphs
  ```

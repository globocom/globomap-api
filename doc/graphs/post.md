# Create Graphs

----
  Create Graph in DB.

* **URL**

  /v1/graphs

* **Method:**

  `POST`

* **Data Params**

  `{"name":"graph1","links":[{"edge":"edge1","from_collections":["coll1"],"to_collections":["coll2"]},{"edge":"edge2","from_collections":["coll2"],"to_collections":["coll3"]}]}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{}`
 
* **Error Response:**

  * **Code:**: 500
  * **Content:**: `{"errors": "Cannot create graph graph1, duplicate name."}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors": "Some message informing that JSON is malformed"}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X POST -d '{"name":"graph1","links":[{"edge":"edge1","from_collections":["coll1"],"to_collections":["coll2"]},{"edge":"edge2","from_collections":["coll2"],"to_collections":["coll3"]}]}' http://localhost:5000/v1/graphs
  ```
  
* **Notes:**

  If the edges or collections passed don't exist, they will be automatically created.

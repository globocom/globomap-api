# Create Graphs

----
  Create Graphs in DB.

* **URL**

  /v1/graphs

* **Method:**

  `POST`

* **Data Params**

  `{"name":"abc1","links":[{"edge":"edge1","from_collections":["coll1"],"to_collections":["coll2"]}]}`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{}`

* **Sample Call:**

  ```shell
     curl http://localhost:8000/v1/graphs
  ```

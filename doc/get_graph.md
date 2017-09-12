# List Graphs

----
  Returns json data with list of graphs in DB.

* **URL**

  /v1/graphs

* **Method:**

  `GET`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"links": [{ "edge": "edge_1", "from_collections": ["collection_1"], "to_collections": ["collection_2"]}]}]`

* **Sample Call:**

  ```shell
     curl http://localhost:8000/v1/graphs
  ```

# Delete connections between documents in collections

----
  Delete connection between two documents in collections in DB.

* **URL**

  /v1/edges/<edge>/<key>

* **Method:**

  `DELETE`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `{}`
  
  OR
  
  * **Code:** 404
  * **Content:** `{"errors":"There no document with key provider2_1"}`

* **Sample Call:**

  ```shell
     curl -X DELETE http://localhost:5000/v1/edges/edge1/provider2_1
  ```
  

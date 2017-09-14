# Delete documents in Collections

----
  Delete document in collection.

* **URL**

  /v1/collections/<collection>/<key>

* **Method:**

  `DELETE`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `{}`
  
  OR
  
  * **Code:** 404
  * **Content:** `{"errors":"There no document with key provider1_1"}`

* **Sample Call:**

  ```shell
     curl -X DELETE http://localhost:5000/v1/collections/coll1/provider1_1
  ```
  

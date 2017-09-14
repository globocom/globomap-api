# List informations of Document in Collection

----
  Returns json data with list of information of Document in Collection.

* **URL**

  /v1/collections/<collection>/<key>

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_id":"coll1/provider1_1","_key":"provider1_1","_rev":"_VmAEYzW---","id":"1","metadata":null,"name":"document-in-coll1","properties":{"anykey":"anyvalue"},"provider":"provider1","timestamp":1501543772}`
  
  OR
  
  * **Code:** 404
  * **Content:** `{"errors":"There no document with key provider1_1"}`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/collections/coll1/provider1_1
  ```
  

# List Documents in Collections

----
  Returns json data with all documents of collection in DB.

* **URL**

  /v1/edges/<edge>

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `[{"_id":"coll1/provider1_2","_key":"provider1_2","_rev":"_VmA8DvC---","id":"2","metadata":null,"name":"document-in-coll2","properties":{"anykey2":"anyvalue2"},"provider":"provider1","timestamp":1501543772},{"_id":"coll1/provider1_1","_key":"provider1_1","_rev":"_VmA7wH----","id":"1","metadata":null,"name":"document-in-coll1","properties":{"anykey":"anyvalue"},"provider":"provider1","timestamp":1501543772}]`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/edges/edge1
  ```
# List Documents in Collections

----
  Returns json data with all documents of collection in DB.

* **URL**

  /v1/edges/<edge>

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `[{"_from":"coll1/provider1_1","_id":"edge1/provider1_1","_key":"provider1_1","_rev":"_VmCLxme---","_to":"coll1/provider1_2","id":"1","metadata":null,"name":"link1","properties":{"anykey":"anyvalue"},"provider":"provider1","timestamp":1501543772},{"_from":"coll2/provider1_1","_id":"edge2/provider1_1","_key":"provider1_2","_rev":"_VmCLxme---","_to":"coll2/provider1_2","id":"2","metadata":null,"name":"link2","properties":{"anykey":"anyvalue"},"provider":"provider1","timestamp":1501543772}]`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/edges/edge1
  ```

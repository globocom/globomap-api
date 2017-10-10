# List informations of about connection between documents

----
  Returns json data with information of a connection between two documents in collections.

* **URL**

  /v1/edges/<edge>/<key>

* **Method:**

  `GET`
  
* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_from":"coll1/provider1_1","_id":"edge1/provider2_1","_key":"provider2_1","_rev":"_VmBC5Re---","_to":"coll2/provider1_1","id":"1","metadata":null,"name":"connection-between-documents","properties":{"anykey":"anyvalue"},"provider":"provider2","timestamp":1501543772}`
  
  OR
  
  * **Code:** 404
  * **Content:** `{"errors":"There no document with key provider2_1"}`

* **Sample Call:**

  ```shell
     curl http://localhost:5000/v1/edges/edge1/provider2_1
  ```
  

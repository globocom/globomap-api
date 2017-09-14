# Connect two documents using Edge

----
  Create connection between two documents using Edge in DB.

* **URL**

  /v1/edges/<edge>

* **Method:**

  `POST`

* **Data Params**

  `{"from":"coll1/provider1_1","to":"coll2/provider1_1","id":"1","name":"connection-between-documents","provider":"provider2","timestamp":1501543772,"properties":{"anykey":"anyvalue"}}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_id":"edge1/provider2_1","_key":"provider2_1","_rev":"_VmBC5Re---","sync":false}`
 
* **Error Response:**

  * **Code:**: 404
  * **Content:**: `{"errors":"Edge edge1 not found."}`

  OR

  * **Code:**: 400
  * **Content:**: `{"errors":"Cannot create document provider2_1, document already created."}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed."}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X POST -d '{"from":"coll1/provider1_1","to":"coll2/provider1_1","id":"1","name":"connection-between-documents","provider":"provider2","timestamp":1501543772,"properties":{"anykey":"anyvalue"}}' http://localhost:5000/v1/edges/edge1
  ```
  
  

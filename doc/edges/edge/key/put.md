# Updates connections between documents in collections

----
  Update connection between two documents in collections in DB.

* **URL**

  /v1/edges/<edge>/<key>

* **Method:**

  `PUT`

* **Data Params**

  `{"from":"coll1/provider1_1","to":"coll1/provider1_2","id":"1","name":"link","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anyvalue"}}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_id":"edge1/provider1_1","_key":"provider1_1","_old_rev":"_VmCKRLK---","_rev":"_VmCLxme---","sync":false}`
 
* **Error Response:**
  
  * **Code:**: 404
  * **Content:**: `{"errors":"Edge edge1 not found."}`

  OR
  
  * **Code:**: 404
  * **Content:**: `{"errors":"There no document with key provider1_1"}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed."}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X PUT -d '{"from":"coll1/provider1_1","to":"coll1/provider1_2","id":"1","name":"link","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anynewvalue", "newkey":"anyvalue"}}' http://localhost:5000/v1/edges/edge1/provider1_1
  ```

* **Notes:**
  
  Updating connections using PUT will maintain all fields that was not passed in payload and create the others that actually don't exist.

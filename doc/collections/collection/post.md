# Create documents into collection

----
  Create document into collection in DB.

* **URL**

  /v1/collections/<collection>

* **Method:**

  `POST`

* **Data Params**

  `{"id":"1","name":"document-in-coll1","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anyvalue"}}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_id":"coll1/provider1_1","_key":"provider1_1","_rev":"_VmAdGr6---","sync":false}`
 
* **Error Response:**

  * **Code:**: 404
  * **Content:**: `{"errors":"Collection coll1 not found."}`
  
  OR

  * **Code:**: 400
  * **Content:**: `{"errors":"Cannot create document provider1_1, document already created."}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed."}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X POST -d '{"id":"1","name":"document-in-coll1","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anyvalue"}}' http://localhost:5000/v1/collections/coll1
  ```
  
  

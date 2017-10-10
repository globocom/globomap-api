# Updates documents in collections

----
  Update document into collection.

* **URL**

  /v1/collections/<collection>/<key>

* **Method:**

  `PATCH`

* **Data Params**

  `{"id":"2","name":"document-in-coll-updated","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anynewvalue","anynewkey":"newvalue"}}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{"_id":"coll1/provider1_1","_key":"provider1_1","_old_rev":"_VmA0x1K---","_rev":"_VmA2XLe---","sync":false}`
 
* **Error Response:**

  * **Code:**: 404
  * **Content:**: `{"errors":"There no document with key provider1_1"}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed."}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X PATCH -d '{"id":"2","name":"document-in-coll-updated","provider":"provider1","timestamp":1501543772,"properties":{"anykey":"anynewvalue","anynewkey":"newvalue"}}' http://localhost:5000/v1/collections/coll1
  ```

* **Notes:**
  
  Updating document into collection using PATCH will maintain in the document all fields that was not passed in payload and create the others that actually don't exist.

# Create Collections

----
  Create Collection in DB.

* **URL**

  /v1/collections

* **Method:**

  `POST`

* **Data Params**

  `{"name":"coll1"}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{}`
 
* **Error Response:**

  * **Code:**: 500
  * **Content:**: `{"errors":"Cannot create collection coll1, duplicate name."}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed"}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X POST -d '{"name":"coll1"}' http://localhost:5000/v1/collections
  ```


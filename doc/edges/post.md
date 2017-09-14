# Create Edge

----
  Create Edge in DB

* **URL**

  /v1/edges

* **Method:**

  `POST`

* **Data Params**

  `{"name":"edge1"}`

* **Success Response:**

  * **Code:** 200
  * **Content:** `{}`
 
* **Error Response:**

  * **Code:**: 500
  * **Content:**: `{"errors":"Cannot create edge edge1, duplicate name."}`
  
  OR
  
  * **Code:**: 400
  * **Content:** `{"errors":"Some message informing that JSON is malformed."}`

* **Sample Call:**

  ```shell
     curl -H "Content-Type: application/json" -X POST -d '{"name":"edge1"}' http://localhost:5000/v1/edges
  ```


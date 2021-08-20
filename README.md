# sqlite-flask-api

A basic sqlite3 flask API.

---

## TODO
- [ ] C 
- [x] R
- [ ] U, all fields from JSON body
- [x] D

---

### Routes available:

GET http://127.0.0.1:5002/customers
GET http://127.0.0.1:5002/customers/id
PUT http://127.0.0.1:5002/customers/id
DELETE http://127.0.0.1:5002/customers/id

---


```
curl -s http://127.0.0.1:5002/customers/3 | jq

```
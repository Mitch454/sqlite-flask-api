import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

db = ('chinook.db')


def sqlJson(path_to_db, query):
# sql data to list of dicts
      try:
          conn = sqlite3.connect(path_to_db)
          conn.row_factory = sqlite3.Row
          items = conn.execute(query).fetchall()
          unpacked = [{j: item[j] for j in item.keys()} for item in items]
          return jsonify(unpacked)
      except Exception as e:
          print(f"Failed to execute query: {query}\n with error:\n{e}")
          return []
      finally:
          conn.close()


def sqlCmd(path_to_db, updatestr):
# update one
      try:
          conn = sqlite3.connect(path_to_db)
          conn.execute(updatestr)
          conn.commit()
          return jsonify({'message' : 'Success'})
      except Exception as e:
          print(f"Failed to execute query: {updatestr}\n with error:\n{e}")
          return []
      finally:
          conn.close()



class customers(Resource):
# Get all jobs
    def get(self):
        return sqlJson(db, 'SELECT * from customers')


class getCustomer(Resource):
# Get one
    def get(self, id):
        return sqlJson(db, "SELECT * from customers WHERE customerId = '{}' ".format(id) )
        


class update(Resource):
# Update FirstName field of one customer
    def put(self, id):
        json = request.get_json()
        newFirstName = json["FirstName"]
        # print('Updating {} with {}'.format(id, newFirstName))
        return sqlCmd(db, "UPDATE customers SET FirstName = '{}' WHERE customerId = {};".format(newFirstName, id))


class delete(Resource):
# Delete one
    def delete(self, id):
        print('Deleting where id ={}'.format(id))
        return sqlCmd(db, "DELETE FROM customers WHERE customerId = {};".format(id))


@app.route('/', methods=['GET'])
def home():
    return '''<div style="padding:1rem 2rem;font-family:Sans-Serif;">
                <h1>Test API</h1>
                <h3">Basic API for chinook.db</h3>
                <h4>Routes available:</h4>
                <ul><li>GET http://127.0.0.1:5002/customers</li>
                    <li>GET http://127.0.0.1:5002/customers/&lt;id&gt; </li>
                    <li>PUT http://127.0.0.1:5002/customers/&lt;id&gt; </li>
                    <li>DELETE http://127.0.0.1:5002/customers/&lt;id&gt; </li>
              </div>
            '''


@app.errorhandler(404)
def not_found(e):
    data = {'message' : '404 no route found'}
    return jsonify(data)


api.add_resource(customers, '/customers')
api.add_resource(getCustomer, '/customers/<int:id>')
api.add_resource(update, '/customers/<int:id>')
api.add_resource(delete, '/customers/<int:id>')

if __name__ == '__main__':
     app.run(port='5002', use_reloader=True)


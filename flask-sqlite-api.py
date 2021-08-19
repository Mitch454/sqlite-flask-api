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


class customers(Resource):
# Get all jobs
    def get(self):
        print('get all')
        return sqlJson(db, 'SELECT * from customers')
        


class getCustomer(Resource):
# Get one
    def get(self, id):
        print('get one')
        return sqlJson(db, "SELECT * from customers WHERE customerId = '{}' ".format(id) )
        

class update(Resource):
    pass

class delete(Resource):
    pass


@app.route('/', methods=['GET'])
def home():
    return '''<div style="padding:1rem 2rem;font-family:Sans-Serif;">
                <h1>Test API</h1>
                <h3">Basic API for chinook.db</h3>
                <h4>Routes available:</h4>
                <ul><li>http://127.0.0.1:5002/customers</li>
                    <li>http://127.0.0.1:5002/customers/&lt;id&gt; </li>
              </div>
            '''


@app.errorhandler(404)
def not_found(e):
    data = {'message' : '404 no route found'}
    return jsonify(data)


api.add_resource(customers, '/customers')
api.add_resource(getCustomer, '/customers/<int:id>')


if __name__ == '__main__':
     app.run(port='5002', use_reloader=True)


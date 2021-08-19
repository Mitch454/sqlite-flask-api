import sqlite3
# import pyodbc
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify


app = Flask(__name__)
api = Api(app)

db = ('chinook.db')


def sqlJson(path_to_db, select_query):
# sql data to list of dicts
      try:
          conn = sqlite3.connect(path_to_db)
          conn.row_factory = sqlite3.Row
          items = conn.execute(select_query).fetchall()
          unpacked = [{j: item[j] for j in item.keys()} for item in items]
          return jsonify(unpacked)
      except Exception as e:
          print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
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



@app.errorhandler(404)
def not_found(e):
    data = {'data' : 'no route found'}
    return jsonify(data)


@app.route('/', methods=['GET'])
def home():
    return '''  <h1 style="font-family:Sans-Serif; padding:1rem 2rem;">Test API</h1>
                <h3 style="font-family:Sans-Serif; padding:1rem 2rem;">Basic API for chinook.db</h3>'''




api.add_resource(customers, '/customers')
api.add_resource(getCustomer, '/customers/<int:id>')


if __name__ == '__main__':
     app.run(port='5002', use_reloader=True)


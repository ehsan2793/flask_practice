from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {"message": "no item"},404




class ItemList(Resource):
    def get(self):
        return {"items":items}
    def post(self):
        req = request.get_json()
        item = {'name': req['name'], 'price': req['price']}
        items.append(item)
        return item , 201

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/item')
app.run(port=3001 , debug=True)

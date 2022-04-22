from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):

    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404


class ItemList(Resource):
    def get(self):
        return {"items": items}

    def post(self):
        req = request.get_json()
        if next(filter(lambda x: x['name'] == req['name'], items), None) is None:
            item = {'name': req['name'], 'price': req['price']}
            items.append(item)
            return item, 201
        else:
            return {"message": 'name already exists'}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/item')
app.run(port=3001, debug=True)

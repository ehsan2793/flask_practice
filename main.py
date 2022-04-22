from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'I am the secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)
items = [
    {'name': 'ehsan', 'price': 1000}
]


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item else 404

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {"items": items}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("price", type=float, help="dont forget the price", required=True)
        req = parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': req['price']}
            items.append(item)
            return item, 201
        else:
            item.update(req)


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

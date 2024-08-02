from flask import Flask, request
from db import stores, items
from flask_smorest import abort
import uuid

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return { "stores": list(stores.values()) }

@app.post("/stores")
def create_store():
    data = request.get_json()
    if "name" not in data:
        abort(400, message="Ensure 'name' is included in payload")
    
    for store in stores.values():
        if data["name"] == store["name"]:
            abort(400, message="Store already exists")

    store_id = uuid.uuid4().hex
    new_store = { **data, "id": store_id }
    stores[store_id] = new_store
    return new_store, 201

@app.get("/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found")

@app.delete("/stores/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return { "message": "Store deleted"}, 200
    except KeyError:
        abort(404, message="Store not found")

@app.get("/items")
def get_items():
    return { "items": list(items.values()) }

@app.post("/items")
def create_item():
    data = request.get_json()
    if (
        "price" not in data or "store_id" not in data or "name" not in data
    ):
        abort(400, message="Ensure 'price', 'name' and 'store_id' are included")

    if data["store_id"] not in stores:
        abort(404, message="Store not found")
    for item in items.values():
        if data["name"] == item["name"] and data["store_id"] == item["store_id"]:
            abort(400, message="Item already exists in store")

    item_id = uuid.uuid4().hex
    item = { **data, "id": item_id }
    items[item_id] = item
    return item, 201
    

@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found")

@app.delete("/items/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return { "message": "Item deleted"}, 200
    except KeyError:
        abort(404, message="Item not found")

@app.put("/items/<string:item_id>")
def update_item(item_id):
    data = request.get_json()
    if "price" not in data or "name" not in data:
        abort(400, message="Ensure 'price' and 'name' are included")
    
    try:
        item = items[item_id]
        item |= data # in place update of dict operator |=
        item["id"] = item_id
        return item, 200
    except KeyError:
        abort(404, message="Item not found")
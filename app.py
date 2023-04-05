import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

#create Flask app (application) --> flask run
app = Flask(__name__)

########################
##### FLASK ROUTES #####
########################

# create an GET end pt (a.k.a Flask route)
@app.get("/stores")
def get_stores():
    return {'stores': list(stores.values())}

#create a POST endpt for /store
@app.post("/store")
def create_store():
    """POST a store to our stores dict"""
    #first we need to get the JSON the client has sent us - request is a module from the flask package
    store_data = request.get_json()
    
    ### ERROR HANDLEING ###
    if 'name' not in store_data:
        abort(404,
              message="Bad request. Ensure 'name' is inculded in JSON payload.")
    ### CHECK store doesnt already exist!
    for store in stores.items():
        if store_data['name'] == store['name']:
            abort(404, message='Store already exists!')
    #create a unique_id 
    store_id = uuid.uuid4().hex
    #create new object to append to stores list
    new_store = {**store_data, 'id': store_id} #** unpack the kwargs + add our id to dict
    stores[store_id] = new_store # add new_store to our stores db
    return new_store, 201 #200 is default status code - OK | 201 means success and created resource (new_store)


@app.post("/item")
def create_item():
    #grab incoming data
    item_data = request.get_json()
    
    ### ERROR HANDLING - will check types with marshmallow later ###
    if (
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        abort(404,
              message="Bad Request. Ensure 'price', 'store_id' and 'name' are present in payload.")
    
    #### CHECK that item doesnt already exist
    for item in items.values():
        if (
            item_data["name"] == item["name"] and
            item_data["store_id"] == item["store_id"]
        ):
            abort(404,
                  message='Item already exists within that store.')
    
    if item_data['store_id'] not in stores: #check if we have a matching key in our stores dict
        abort(404, message='Store not found.') #abort will exit function so no need to return! also helps with documentation
    else:
        # assuming all details are correct
        item_id = uuid.uuid4().hex
        new_item = {**item_data, 'item_id': item_id}
        items[item_id] = new_item
        return new_item, 201

@app.get("/items")
def get_all_items():
    return {'items': list(items.values())}


#get a specific stores data - based on /<string:name> endpt
@app.get("/store/<string:store_id>")
def get_store_name(store_id):
    try:
        return stores[store_id]
    except KeyError as e:
        abort(404, message="Store name not found.")

#get A specific stores items - based on /<string:name> endpt
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError as e:
        abort(404, message="Item not found.")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message': 'Item deleted'}, 201
    except KeyError as e:
        abort(404, message="Item not found.")

@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': 'Store deleted'}, 201
    except KeyError as e:
        abort(404, message="store not found.")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()

    ### ERROR HANDLEING ###
    if "name" not in item_data or "price" not in item_data:
        abort(404,
              message="Bad Request. Ensure 'name' and 'price' are in JSON Payload.")

    try:
        item = items[item_id]
        print('here')
        item |= item_data #new dictionary update inplace method |= it merges the two dict - if keys exist they are replaced!
        return item
    except KeyError as e:
        abort(404,
              message="Item not found.")
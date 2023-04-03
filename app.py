import uuid
from flask import Flask, request
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
    if item_data['store_id'] not in stores: #check if we have a matching key in our stores dict
        return {'message': 'store not found'}, 404
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
        return {"message": "Store name not found!"}, 404

#get A specific stores items - based on /<string:name> endpt
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError as e:
        return {'message': 'item not found'}, 404
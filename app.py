from flask import Flask, request

#create Flask app (application) --> flask run
app = Flask(__name__)


#####################
##### DATASTORE #####
#####################
#defining where to store data. Right now we store in a list, but in future use DB
#obviuosly every time we close app - we lose all data we have posted since python lists
#dont persist - theyre stored in memory and once app closes memory is wiped

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

########################
##### FLASK ROUTES #####
########################

# create an GET end pt (a.k.a Flask route) /store
@app.get("/stores")
def get_stores():
    #when endpt is called at http://127.0.0.1:5000
    #flask will run view fun and return the data.
    return {"stores": stores}

#create a POST endpt for /store
@app.post("/store")
def create_store():
    """POST a store to our stores list"""
    #first we need to get the JSON the client has sent us - request is a module from the flask package
    request_data = request.get_json()
    #create new object to append to stores list
    new_store = {"name": request_data["name"], "items": []} #we will add items later
    stores.append(new_store)
    return new_store, 201 #200 is default status code - OK | 201 means success and created resource (new_store)


#creating a POST request which takes as endpoint /store then the store's name (in this case My Store) that we want
#to post new item too and /items
@app.post("/store/<string:name>/item") #NO SPACES
def create_item(name):
    #grab incoming data
    request_data = request.get_json()
    #look through our stores list and find the store that matches name
    for store in stores:
        if store["name"] == name:
            #create a dict of new item
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            #add that item to the specific stores items list
            store["items"].append(new_item)
            return new_item, 201 #return all good 201
    #else we want to return a message to the client
    return {"message": "Store not found"}, 404

#get a specific stores data - based on /<string:name> endpt
@app.get("/store/<string:name>")
def get_store_name(name):
    for store in stores:
        if store["name"] == name:
            return store, 201
    return {"message": "Store name not found!"}, 404

#get A specific stores items - based on /<string:name> endpt
@app.get("/store/<string:name>/items")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}, 201
    return {"message": "Store name not found!"}, 404
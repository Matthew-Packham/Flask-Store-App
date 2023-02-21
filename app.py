from flask import Flask

#create Flask app (application) --> flask run
app = Flask(__name__)

#defining where to store data. Right now we store in a list, but in future use DB
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

# create an end pt(a.k.a Flask route) /store
@app.get("/store")
def get_stores():
    #when endpt is called at http://127.0.0.1:5000
    #flask will run fun and return the data.
    return {"stores": stores}
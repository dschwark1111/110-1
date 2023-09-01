from flask import Flask, request, abort 
from config import me, db
import json
from bson import ObjectId
from flask_cors import CORS
#creates server
app = Flask("server")
CORS(app) #warning this line will disable cors

@app.get("/")
def home():
    return "Hello World"

@app.get("/test")
def test():
    return "this is a test page"

@app.get("/about")
def about():
    return "Dottie"


#####################API PRODUCTS
##USE JSON

@app.get("/api/about/developer")
def developer():
    full_name = me["name"] + " " + me["last_name"]
    return json.dumps(full_name)


@app.get("/api/aboutus")
def aboutus_data():
    return json.dumps(me)

@app.get("/api/categories")
def categories():
    all_cats = []
    cursor = db.products.find({})
    for products in cursor: 
        category = products["category"]
        if category not in all_cats:
            all_cats.append(products["category"])
    return json.dumps (all_cats)

def fix_id(record):
    record["_id"] = str(record ["_id"])
    return record

@app.get("/api/products")
def get_products():
    products = []
    cursor = db.products.find({})
    for product in cursor: 
        products.append(fix_id(product))

    return json.dumps(products)


@app.post("/api/products")
def save_product():
    product = request.get_json()
    db.products.insert_one(product)
    print(product)
    return json.dumps(fix_id(product))

@app.get("/api/products/category/<cat>")
def get_by_category(cat):
    products = []
    cursor = db.products.find({"category": cat})
    for prod in cursor:
        products.append(fix_id(prod))
    return json.dumps(products)

@app.get("/api/products/id/<id>")
def get_product_id(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")
    db_id = ObjectId
    product = db.products.find_one ({"_id": db_id})
    if not product:
        return about (404, "product not found")
    
    return json.dumps(product)

@app.delete("/api/products/id/<id>")
def delete_product(id):
    if not ObjectId.is_valid(id):
        return abort(400, "Invalid ID")
    db_id = ObjectId (id)
    db.products.delete_one ({"_id": id})
    
    return json.dumps({"status": "OK"})

@app.get("/api/reports/total")
def total_value():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(f"The total value is ${total}")


@app.get("/api/coupons")
def coupon_code():
    results = []
    cursor = db.coupons.find({})
    for coupon in cursor:
        results.append(fix_id(coupon))

    return json.dumps(results)

@app.post("/api/coupons")
def save_coupon():
    coupon = request.get_json()

    #MUST HAVE CODE
    if not "code" in coupon: 
        return about (400, "code is required")
    #MUST HAVE DISCOUNT
    if not "discount" in coupon:
        return about (400, "discount is required")
    #discount can't be bigger than 35


    db.coupons.insert_one(coupon)
    return json.dumps(fix_id(coupon))



@app.get("/api/coupons/code/<code>")
def get_coupon_code(code):
    coupon = db.coupons.find_one({"code":code})
    if not coupon:
        return abort (404, "coupon not found")
    
    return json.dumps(fix_id(coupon))

@app.get("/api/coupons/id/<id>")
def get_coupon_id(id):
    if not ObjectId.is_valid(id):
        return abort (400, "Invalid ID")

    db_id = ObjectId(id)
    id = db.coupons.find_one({"_id": db_id})
    if not id:
        return abort (404, "coupon not found")
    
    return json.dumps(fix_id(id))








#start server
app.run(debug=True)

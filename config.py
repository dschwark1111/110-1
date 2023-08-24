import pymongo
import certifi

me = {
    "name": "Dottie",
    "last_name": "Schwark",
    "age": "41",
    "hobbies": [],
    "address": {
        "street": "pine drive",
        "city": "that city",
        "zip": "90210",
    }
}

#database config
con_str = "mongodb+srv://dorothyschwark:vrE4IzanrSo2Fd9K@cluster0.3m1knyl.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("grace")

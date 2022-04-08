import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from routes import routes
app = Flask(__name__)
CORS(app)
print("\n\n********* Environment variable Start \n\n")

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', 'dmfuser')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', 'dmfpassword')
MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME', 'mongod')
MONGODB_PORT = os.getenv('MONGODB_PORT', 27017)
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'dmfdb')
MONGODB_URL = os.getenv('MONGO_URL', "DUMMY")
print("MONGODB_USERNAME",MONGODB_USERNAME, " MONGODB_PASSWORD ", MONGODB_PASSWORD, "  MONGODB_HOSTNAME",MONGODB_HOSTNAME)
print("MONGODB_DATABASE ",MONGODB_DATABASE)
print ("MONGODB_PORT", MONGODB_PORT)
print("MONGODB_URL ", MONGODB_URL)
print("\n\n********* updated by 30Environment variable End \n\n")
#mongourl ='mongodb://' + MONGODB_USERNAME + ':' + MONGODB_PASSWORD + '@' + MONGODB_HOSTNAME + ':27017/'
mongourl ="mongodb://"+MONGODB_USERNAME+":"+MONGODB_PASSWORD+"@"+MONGODB_HOSTNAME+":"+MONGODB_PORT+"/?authSource="+MONGODB_DATABASE+"&authMechanism=SCRAM-SHA-256"


print ("\n\n\n\nmongourl" ,mongourl, "mongourl end\n\n\n")
client = MongoClient(mongourl)

databse_name=client[MONGODB_DATABASE]
user_collection=databse_name.dmfuser
tenants_collection=databse_name.tenants
app.config["USER_COLLECTION"]=user_collection
app.config["TENANTS_COLLECTION"]=tenants_collection
"""Add all routes to blueprint this will register"""
app.register_blueprint(routes)
@app.route('/k8demo/<name>')
def get_product(name):
  return "The demo is " + str(name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
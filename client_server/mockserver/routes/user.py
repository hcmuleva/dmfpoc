from datetime import datetime
from flask import request, jsonify
from bson import ObjectId,json_util
from utils.user_auth import *
import json
from . import routes
from flask import current_app
from pymongo import MongoClient

from flask_bcrypt import Bcrypt
bc = Bcrypt()

@routes.route('/ping', methods=['GET'])
def pingservice():
    print("main jind")
    return "Service is up and running"
@routes.route('/apiuser/user/userlist', methods=['GET'])
def userlist():
    print("main jind")
    user_collection = current_app.config["USER_COLLECTION"]
    user_data=user_collection.find_one({})
    #user_data=list(user_collection.find({}))
    page_sanitized = json.loads(json_util.dumps({"userlist":user_data}))
    return page_sanitized,201

@routes.route('/apiuser/user/allusers',methods=['GET'])
def user_list():
    bearertoken = request.headers.get('Accesstoken')
    print("Recieved Token ", bearertoken)
    jwt_arr = bearertoken.split('Bearer ')
    print("allusers jwt_arr ", jwt_arr)
    payload = decode_auth_token(jwt_arr[1])
    if(payload):
        user_collection = current_app.config["USER_COLLECTION"]
        if("user_id" in payload):
            user_id = payload['user_id']
            myarray=[]
            user_data=list(user_collection.find())
            page_sanitized = json.loads(json_util.dumps({"userlist":user_data}))
            return page_sanitized,201
        else:
            page_sanitized = json.loads({"Error":"Invalid User"})
            return page_sanitized, 404
    return {"error":"Error in get all user"}, 404



@routes.route('/apiuser/user/me', methods=["GET","POST"])
def user_profile():
    bearertoken = request.headers.get('Accesstoken')
    jwt_arr=bearertoken.split('Bearer ')
    payload = decode_auth_token(jwt_arr[1])
    user_id=payload['user_id']
    user_collection = current_app.config["USER_COLLECTION"]
    user_in_db = user_collection.find_one({'user_id': user_id})
    page_sanitized = json.loads(json_util.dumps(user_in_db))
    return jsonify({"user": page_sanitized}), 201

@routes.route('/apiuser/user/login', methods=["POST"])
def user_login():
    user_data = request.get_json()
    print("Request recieved ",user_data)
    user_collection = current_app.config["USER_COLLECTION"]
    user_in_db = user_collection.find_one({'user_id': str(user_data['user_id'])})
    print("user_in_db ",user_in_db)
    if user_in_db:
        if bc.check_password_hash(user_in_db['password'], user_data['password']):
            print("Password verified ")
            jwt = encode_auth_token(user_data['user_id'], user_in_db["user_role"])
            print("Token created ",jwt)
            response_data_before_sanitized={"Accesstoken": jwt, "user_role": user_in_db["user_role"], "user": user_in_db}
            print("response_data_before_sanitized", response_data_before_sanitized)
            page_sanitized = json.loads(json_util.dumps(response_data_before_sanitized))
            print("Response sending to client",page_sanitized)
            return jsonify(page_sanitized), 201
        else:
            return jsonify({"Error":"User name or password mismatch"}),401
    else:
        return jsonify({"Error":"User name or password mismatch"}),401
@routes.route('/apiuser/user/register',methods=["POST"])
def user_registration():
    user_data=request.get_json()
    
    print("Recieved headers ", request.headers)
    if 'user_id' not in user_data  or 'password' not in user_data  :
        return jsonify({"message": "Not Acceptable request"}), 406
    if user_data['user_id'] is None or user_data['password'] is None:
        return jsonify({"message": "Not Acceptable request"}), 406

    print("REgistration data",user_data)
    user_collection = current_app.config["USER_COLLECTION"]
    existing_user = user_collection.find_one({'user_id': user_data['user_id']}, {'_id': 0})
    if existing_user:
        print("User already exist ")
        return jsonify({"message": "UserId already exist"}), 409
    if existing_user is None:
        if("user_role" not in user_data):
            user_data["user_role"]=[{"role":"user"}]
        hashpass = bc.generate_password_hash(user_data['password']).decode('utf-8')
        user_data['password'] = hashpass
        user_collection.insert_one(user_data)
    jwt = encode_auth_token(user_data['user_id'], user_data["user_role"])
    resp_before_sanitized={"message":"successfully registered user","Accesstoken": jwt, "user_role": [{"role":"user"}], "user": user_data}
    page_sanitized = json.loads(json_util.dumps(resp_before_sanitized))
    return jsonify(page_sanitized), 201

@routes.route('/apiuser/user/update',methods=["PUT"])
def user_update():
    user_data=request.get_json()
    print("Recieved headers ", request.headers)
    bearertoken = request.headers.get('Accesstoken')
    print("Recieved Token ", bearertoken)
    jwt_arr = bearertoken.split('Bearer ')
    print("jwt_arr ", jwt_arr)
    payload = decode_auth_token(jwt_arr[1])
    print("payload ",payload)
    user_id = payload['user_id']
    user_collection = current_app.config["USER_COLLECTION"]
    user_in_db = user_collection.find_one({'user_id': user_id})
    #del user_data['headers']
    if user_in_db is None:
        print("User does not exist ")
        return jsonify({"message": "UserId does not exist"}), 404
    if user_in_db:
        if ("password" in user_data):
            hashpass = bc.generate_password_hash(user_data['password']).decode('utf-8')
            user_data['password'] = hashpass
    if ("user_role" not in user_data):
        user_data["user_role"] = [{"role": "user"}]
    user_collection = current_app.config["USER_COLLECTION"]
    user_collection.find_one_and_update({'_id': user_in_db["_id"]}, {"$set": user_data}, upsert=False)
    updated_user_data = user_collection.find_one({'user_id':user_id}, {"_id":0,"password":0})
    print("updated_user_data",updated_user_data)
    return jsonify({"message":"Successfully updated user profile","user": updated_user_data, "Accesstoken":jwt_arr[0]}),201

@routes.route('/apiuser/user/delete',methods=["DELETE"])
def user_delete():
    print("Recieved headers ", request.headers)
    bearertoken = request.headers.get('Accesstoken')
    print("Recieved Token ", bearertoken)
    jwt_arr = bearertoken.split('Bearer ')
    print("jwt_arr ", jwt_arr)
    payload = decode_auth_token(jwt_arr[1])
    user_id = payload['user_id']
    user_collection = current_app.config["USER_COLLECTION"]
    existing_user = user_collection.find_one({'user_id': user_id})
    if existing_user is None:
        return jsonify({"message": "UserId does not exist"}), 404
    if existing_user:
        user_collection.delete_one({'user_id': user_id})
    return jsonify({"message":"Successfully Delete user profile"}),204

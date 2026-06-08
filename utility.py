
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request,session

from db import *
def check_user():
    username=request.form["username"]
    password=request.form["password"]
    datas=check_db(username)
    if datas:
        id=datas.get("id")
        session["id"]=id
        name=datas.get("name")
        session["name"]=name
        db_password=datas.get("password")
        if check_password_hash(db_password,password):
            return True
        else:
            return False
    else:
        return False
def register():
    username=request.form["username"]
    name=request.form["name"]
    password=request.form["password"]
    hashed_password = generate_password_hash(password)
    return store_user(username,name,hashed_password)
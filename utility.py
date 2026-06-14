from unittest import result

from werkzeug.security import generate_password_hash, check_password_hash
from flask import request,session
from werkzeug.utils import secure_filename
import uuid
import os
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

def item_form(form_type):
    item_name=request.form["item_name"]
    description=request.form["description"]
    lost_location=request.form["location"]
    lost_date=request.form["date"]
    receiver_number=request.form["mobile_number"]
    user_id = session.get("id")
    image = request.files["image"]
    filename=f"{uuid.uuid4()}_{secure_filename(image.filename)}"
    image.save(os.path.join("static/uploads",filename))
    image_location=f"uploads/{filename}"
    if form_type == "lost":
        result=store_items(user_id,item_name,description,lost_location,lost_date,image_location,receiver_number,form_type)
        return result
    elif form_type == "found":
        result=store_items(user_id,item_name,description,lost_location,lost_date,image_location,receiver_number,form_type)
        return result

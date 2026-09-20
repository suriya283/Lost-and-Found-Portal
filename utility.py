

from werkzeug.security import generate_password_hash, check_password_hash
from flask import request,session
from werkzeug.utils import secure_filename
import uuid
import os
from db import *
def check_user():
    username=request.form["username"]
    password=request.form["password"]
    admin = check_admin(username)
    datas = check_db(username)
    if admin:
        db_password=admin.get("password")
        if check_password_hash(db_password,password):
            id = admin.get("id")
            name = admin.get("username")
            session["adminId"] = id
            session["adminName"] = name
            return "admin"
    elif datas:
        db_password=datas.get("password")
        if check_password_hash(db_password,password):
            id = datas.get("id")
            name = datas.get("name")
            session["id"] = id
            session["name"] = name
            return "user"
        else:
            return
    else:
        return
def register():
    username=request.form["username"]
    name=request.form["name"]
    password=request.form["password"]
    hashed_password = generate_password_hash(password)
    return store_user(username,name,hashed_password)

def item_form(form_type):
    item_name=request.form["item_name"]
    description=request.form["description"]
    verification_des=request.form["verification_description"]
    lost_location=request.form["location"]
    lost_date=request.form["date"]
    receiver_number=request.form["mobile_number"]
    user_id = session.get("id")
    image_location=None
    if request.files["image"]:
        image = request.files["image"]
        filename=f"{uuid.uuid4()}_{secure_filename(image.filename)}"
        image.save(os.path.join("static/uploads",filename))
        image_location=f"uploads/{filename}"
    if form_type == "lost":
        result=store_items(user_id,item_name,description,verification_des,lost_location,lost_date,receiver_number,form_type,image_location)
        return result
    elif form_type == "found":
        result=store_items(user_id,item_name,description,verification_des,lost_location,lost_date,receiver_number,form_type,image_location)
        return result
def claim_details():
    proof=request.form["proof"]
    id=request.form["item_id"]
    user_id=session.get("id")
    return store_proof(id,proof,user_id)
def founder():
    number=request.form["number"]
    location = request.form["location"]
    user_id=session.get("id")
    id = request.form["item_id"]
    description = request.form["description"]
    return(store_founder(user_id,id,number,location,description))
print(generate_password_hash("suriya123"))
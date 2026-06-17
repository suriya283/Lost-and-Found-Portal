from unittest import result

from _testcapi import error

from utility import *
from db import *
from flask import Flask, render_template, request, flash, redirect,session

app=Flask(__name__)
app.secret_key="12345"

UPLOAD_FOLDER="static/uploads"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
@app.route('/')
def login():
    return render_template("index.html")

@app.route("/signin", methods=['POST','GET'])
def signin():
    if request.method=="POST":
        res=check_user()
        if res:
            flash(f"{session.get('name')} You are successfully logged in","success")
            return redirect("/home")
        else:
            flash("Username or password is incorrect","error")
            return redirect("/")
    return render_template("index.html")
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        if register():
            flash("Username is already exists!","error")
            return redirect("/")
        else:
            flash("Successfully registered!","success")
            return redirect("/")
    return render_template("index.html")
@app.route("/home",methods=["GET","POST"])
def home():
    search=request.args.get("search")
    status=request.args.get("filter")
    if search:
        datas=search_items(search,status)
    else:
        datas=get_all_item()
    lost_count=sum(1 for item in datas if item["status"]=="lost")
    found_count=sum(1 for item in datas if item["status"]=="found")
    return render_template("home.html",datas=datas,lost_count=lost_count,found_count=found_count)
@app.route("/report",methods=["GET","POST"])
def report_item():
    if request.method=="POST":
        form_type=request.form["form_type"]
        if form_type == "lost":
            result=item_form(form_type)
            if result:
                flash("Successfully report the Lost Item!","success")
                return redirect('/home')
        if form_type == "found":
            result=item_form(form_type)
            if result:
                flash("Successfully report the Found Item!","success")
                return redirect('/home')
    return render_template("home.html")
if __name__=="__main__":
    app.run(debug=True)

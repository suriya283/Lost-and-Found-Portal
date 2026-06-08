
from utility import *
from db import *
from flask import Flask, render_template, request, flash, redirect,session

app=Flask(__name__)
app.secret_key="12345"
@app.route('/')
def login():
    return render_template("index.html")

@app.route("/signin", methods=['POST','GET'])
def signin():
    if request.method=="POST":
        res=check_user()
        if res:
            return render_template("home.html",result=f"{session.get('name')} You are successfully logged in")
        else:
            flash("Username or password is incorrect")
            return redirect("/")
    return render_template("index.html")
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        if register():
            flash("Username is already exists!")
            return redirect("/")
        else:
            flash("Successfully registered!")
            return redirect("/")
    return render_template("index.html")
if __name__=="__main__":
    app.run(debug=True)
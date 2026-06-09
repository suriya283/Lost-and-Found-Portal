
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
            flash(f"{session.get('name')} You are successfully logged in")
            return redirect("/home")
        else:
            flash("<span style='color:red;'>Username or password is incorrect </span>")
            return redirect("/")
    return render_template("index.html")
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        if register():
            flash("<span style='color:red;'>Username is already exists! </span>")
            return redirect("/")
        else:
            flash("<span style='color:green;'>Successfully registered! </span>")
            return redirect("/")
    return render_template("index.html")
@app.route("/home",methods=["GET","POST"])
def home():
    return render_template("home.html")
if __name__=="__main__":
    app.run(debug=True)
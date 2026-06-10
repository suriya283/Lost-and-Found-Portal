
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
    lost_items = get_lost_items()
    found_items = get_found_items()
    return render_template("home.html", lost_items=lost_items, found_items=found_items)

@app.route("/lostitem", methods=["POST"])
def lostitem():
    if 'id' not in session:
        flash("<span style='color:red;'>Please login first</span>")
        return redirect("/")
    
    item_name = request.form.get("item name")
    description = request.form.get("description")
    location = request.form.get("lost location")
    date_lost = request.form.get("lost date")
    mobile_number = request.form.get("reciever number")
    user_id = session.get('id')
    
    if store_lost_item(item_name, description, location, date_lost, user_id, mobile_number):
        flash(f"<span style='color:green;'>Lost item '{item_name}' reported successfully!</span>")
    else:
        flash(f"<span style='color:red;'>Failed to report lost item. Please try again.</span>")
    
    return redirect("/home")

@app.route("/founditem", methods=["POST"])
def founditem():
    if 'id' not in session:
        flash("<span style='color:red;'>Please login first</span>")
        return redirect("/")
    
    item_name = request.form.get("found item")
    description = request.form.get("found description")
    location = request.form.get("found location")
    date_found = request.form.get("found date")
    mobile_number = request.form.get("giver number")
    user_id = session.get('id')
    
    if store_found_item(item_name, description, location, date_found, user_id, mobile_number):
        flash(f"<span style='color:green;'>Found item '{item_name}' reported successfully!</span>")
    else:
        flash(f"<span style='color:red;'>Failed to report found item. Please try again.</span>")
    
    return redirect("/home")

if __name__=="__main__":
    app.run(debug=True)
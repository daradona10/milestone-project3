import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# connecting to the database

app.config["MONGO_DBNAME"] = 'Milestone-Project3'
app.config["MONGO_URI"] = 'mongodb+srv://daradona10:maradona1986@myfirstcluster-agrgt.mongodb.net/Milestone-Project3?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route("/")
def get_meals():
    return render_template("meals.html")
  
@app.route("/get_starters")
def get_starters():
    starters_dishes = mongo.db.recipes.find({"course_type": "starters"})
    starters = []
    for s in starters_dishes:
        starters.append({
            "name": s["name"],
            "description": s["description"],
            "prep_time": s["prep_time"],
            "cooking_time": s["cooking_time"],
            "makes": s["makes"],
            "ingredients": s["ingredients"],
            "method": s["method"],
            "course_type": s["course_type"]
        })
    return render_template("starters.html", starters=starters)

@app.route("/get_mains")
def get_mains():
    mains_dishes = mongo.db.recipes.find({"course_type": "main courses"})
    mains = []
    for s in mains_dishes:
        mains.append({
            "name": s["name"],
            "description": s["description"],
            "prep_time": s["prep_time"],
            "cooking_time": s["cooking_time"],
            "makes": s["makes"],
            "ingredients": s["ingredients"],
            "method": s["method"],
            "course_type": s["course_type"]
        })
    return render_template("maincourses.html", mains=mains)



@app.route("/get_desserts")
def get_desserts():
    desserts_dishes = mongo.db.recipes.find({"course_type": "desserts"})
    desserts = []
    for s in desserts_dishes:
        desserts.append({
            "name": s["name"],
            "description": s["description"],
            "prep_time": s["prep_time"],
            "cooking_time": s["cooking_time"],
            "makes": s["makes"],
            "ingredients": s["ingredients"],
            "method": s["method"],
            "course_type": s["course_type"]
        })
        
    return render_template("desserts.html", desserts=desserts)  

@app.route("/get_sides")
def get_sides():
    sides_dishes = mongo.db.recipes.find({"course_type": "sides"})
    sides = []
    for s in sides_dishes:
        sides.append({
            "name": s["name"],
            "description": s["description"],
            "prep_time": s["prep_time"],
            "cooking_time": s["cooking_time"],
            "makes": s["makes"],
            "ingredients": s["ingredients"],
            "method": s["method"],
            "course_type": s["course_type"]
        })
        
    return render_template("sides.html", sides=sides)  

@app.route("/add_meal")
def add_meal():
    return render_template("addmeal.html",
    course_type=mongo.db.course_type.find())      

@app.route("/insert_meal", methods=["POST"])
def insert_meal():
    meals = mongo.db.meals
    meals.insert_one(request.form.to_dict())
    return redirect(url_for('get_meals'))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=5000,
            debug=True) 
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
@app.route('/get_meals')
def get_meals():
    return render_template("meals.html", recipes=mongo.db.recipes.find())

@app.route('/add_recipe')
def add_recipe():
        course_type = mongo.db.course_type.find()
        cooking_time = mongo.db.cooking_time.find()
        return render_template('add_meal.html', course_type=course_type, cooking_time=cooking_time)

@app.route('/insert_recipe', methods=["GET", "POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one( {
        'recipe_name': request.form.get('recipe_name'),
        'recipe_description' : request.form.get('recipe_description'),
        'prep_time' : request.form.get('prep_time'),
        'cooking_time' : request.form.get('cooking_time'),
        'recipe_makes' : request.form.get('recipe_makes'),
        'recipe_ingredients' : request.form.get('recipe_ingredients'),
        'recipe_method' : request.form.get('recipe_method'),
        'course_type' : request.form.get('course_type'),
    })
    return redirect(url_for('get_meals'))
                             
@app.route("/get_mains")
def get_mains():
    return render_template("maincourses.html", all_recipes = mongo.db.all_recipes.find())   

@app.route("/get_starters")
def get_starters():
    return render_template("starters.html", all_recipes = mongo.db.all_recipes.find()) 

@app.route("/get_desserts")
def get_desserts():
    return render_template("desserts.html", all_recipes = mongo.db.all_recipes.find())   

@app.route("/get_sides")
def get_sides():
    return render_template("sides.html", all_recipes = mongo.db.all_recipes.find())  

@app.route("/add_meal")
def add_meal():
    return render_template("add_meal.html")       


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) 
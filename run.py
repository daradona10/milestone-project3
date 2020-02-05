import os
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from flask import request, redirect, url_for
from bson.objectid import ObjectId
import boto3

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://daradona10:maradona1986@myfirstcluster-agrgt.mongodb.net/Milestone-Project3?retryWrites=true&w=majority"
mongo = PyMongo(app)

UPLOAD_FOLDER = "recipe_images"

@app.route("/")
def get_meals():
    return render_template("meals.html")

@app.route("/get_mains")
def get_mains():
    starters = get_recipes_by_type('main courses')
    course_types = get_course_types()
    return render_template("maincourses.html", dishes=starters, course_types=course_types)

def get_course_types():
    return ['starters', 'main courses', 'sides', 'desserts']

def get_recipes_by_type(recipe_type):
    recipes_in_db = mongo.db.recipes.find({"course_type": recipe_type})
    recipes = []
    for s in recipes_in_db:
        recipes.append({
            "dish_id": str(s["_id"]),
            "name": s["name"],
            "description": s["description"],
            "prep_time": s["prep_time"],
            "cooking_time": s["cooking_time"],
            "makes": s["makes"],
            "ingredients": s["ingredients"],
            "method": s["method"],
            "course_type": s["course_type"],
            "image_path": "https://daradona-milestone-project3.s3.amazonaws.com/" + s["image_path"] if "image_path" in s else ""
        })
    
    return recipes

@app.route("/get_starters")
def get_starters():
    starters = get_recipes_by_type('starters')
    course_types = get_course_types()
    return render_template("starters.html", dishes=starters, course_types=course_types)

@app.route("/get_desserts")
def get_desserts():
    desserts = get_recipes_by_type('desserts')
    course_types = get_course_types()
    return render_template("desserts.html", dishes=desserts, course_types=course_types)  

@app.route("/get_sides")
def get_sides():
    sides = get_recipes_by_type('sides')
    course_types = get_course_types()
    return render_template("sides.html", dishes=sides, course_types=course_types)

@app.route("/add_meal")
def add_meal():
    course_types = get_course_types()
    return render_template("add_meal.html", course_types=course_types)

def upload_file_to_s3(filename):
    print('Uploading file to s3')
    try:
        s3_client = boto3.client('s3',
            aws_access_key_id='AKIASIXFUF7B5ETRWRH5',
            aws_secret_access_key='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',
        )
        s3_client.upload_file(filename, 'daradona-milestone-project3', filename, ExtraArgs={'ACL':'public-read'})
    except Exception as e:
        print(e)

    print("Uploaded file successfully!")

@app.route("/add_new_recipe", methods=['GET', 'POST'])
def add_new_recipe():
    name = request.form.get('recipe_name')
    description = request.form.get('description')
    prep_time = request.form.get('prep_time')
    cooking_time = request.form.get('cooking_time')
    makes = request.form.get('makes')
    ingredients = request.form.get('ingredients')
    method = request.form.get('method')
    course_type = request.form.get('course_type')

    f = request.files['file_name']
    file_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(file_path)
    upload_file_to_s3("recipe_images/" + f.filename)

    os.remove(file_path)
    print('Removed local file successfully.')
    
    mongo.db.recipes.insert_one({
        'name': name,
        'description': description,
        'prep_time': prep_time,
        'cooking_time': cooking_time,
        'makes': makes,
        'ingredients': ingredients,
        'method': method,
        'course_type': course_type,
        'image_path': "recipe_images/" + f.filename
    })

    f.close()
    return redirect(url_for('add_meal'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    _recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    course_type = _recipe['course_type']

    mongo.db.recipes.delete_one({
        '_id': ObjectId(recipe_id)
    })

    template = 'get_sides'
    if course_type == 'starters':
        template = 'get_starters'
    elif course_type == 'main courses':
        template = 'get_mains'
    elif course_type == 'desserts':
        template = 'get_desserts'

    return redirect(url_for(template))

@app.route("/update_recipe", methods=['PUT'])
def update_recipe():
    json_body = request.get_json()
    dish_id = json_body["dish_id"]
    dish_type = json_body["dish_type"]
    dish = json_body["dish"]

    myquery = { '_id': ObjectId(dish_id) }
    newvalues = { "$set": dish }
    mongo.db.recipes.update_one(myquery, newvalues)

    dishes = get_recipes_by_type(dish_type)
    course_types = get_course_types()
    return jsonify(dishes = dishes, course_types=course_types)


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    _recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    course_types = get_course_types()

    return render_template('edit_recipe.html', recipe=_recipe, course_types=course_types)


@app.route('/edit_single_recipe/<recipe_id>', methods=['POST'])
def edit_single_recipe(recipe_id):
    course_type = request.form.get('course_type')

    f = request.files['file_name']
    file_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(file_path)
    upload_file_to_s3("recipe_images/" + f.filename)

    os.remove(file_path)
    print('Removed local file successfully.')
    f.close()

    myquery = {'_id': ObjectId(recipe_id)}
    newvalues = {"$set": {
        "dish_id": recipe_id,
        "course_type": course_type,
        "name": request.form.get('recipe_name'),
        "description": request.form.get('description'),
        "prep_time": request.form.get('prep_time'),
        "cooking_time": request.form.get('cooking_time'),
        "makes": request.form.get('makes'),
        "ingredients": request.form.get('ingredients'),
        "method": request.form.get('method'),
        "image_path": "recipe_images/" + f.filename
    }}
    mongo.db.recipes.update_one(myquery, newvalues)

    template = 'get_sides'
    if course_type == 'starters':
        template = 'get_starters'
    elif course_type == 'main courses':
        template = 'get_mains'
    elif course_type == 'desserts':
        template = 'get_desserts'

    return redirect(url_for(template))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=8000, debug=True) 
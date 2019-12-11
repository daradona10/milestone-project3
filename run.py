import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def get_meals():
    return render_template("meals.html")

@app.route("/get_mains")
def get_mains():
    return render_template("maincourses.html")    

@app.route("/get_starters")
def get_starters():
    return render_template("starters.html")

@app.route("/get_desserts")
def get_desserts():
    return render_template("desserts.html")   

@app.route("/get_sides")
def get_sides():
    return render_template("sides.html")  

@app.route("/add_meal")
def add_meal():
    return render_template("add_meal.html")       


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) 
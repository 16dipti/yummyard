from flask import Flask, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# postgres://mysql_7lpf_user:99wXAZtOIYBa7QWAe3NDp24XDKEB6rCL@dpg-cmjle9un7f5s73cchoh0-a.singapore-postgres.render.com/mysql_7lpf

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable = False)
    mobile = db.Column(db.String(80), nullable = False)
    message = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    endpoint = "https://www.themealdb.com/api/json/v1/1/categories.php"

    data = requests.get(endpoint)
    recipes = data.json()['categories']


    area_endpoint = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    request = requests.get(area_endpoint)
    meals = request.json()['meals']


    return render_template('index.html', recipes=recipes, meals=meals)


# contact
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method) == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('phn')
        msg = request.form.get('msg')

        get_message = Contact(
            name = name,
            email = email,
            mobile = mobile,
            message = msg
        )

        db.session.add(get_message)
        db.session.commit()

        return render_template('index.html')


# category
@app.route("/food/<string:category>")
def categories(category):
    enpoint = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    data = requests.get(enpoint)
    meals = data.json()['meals']

    return render_template('category.html', meals=meals, category=category)



# area new
@app.route("/area/<string:area>")
def areas(area):
    enpoint = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"
    data = requests.get(enpoint)
    dish = data.json()['meals']

    return render_template('area2.html', dish=dish, area=area)


def get_ingredients(meal_data):
    ingredients = []
    for i in range(1, 21): 
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"

        if meal_data[0][ingredient_key]:
            ingredient_name = meal_data[0][ingredient_key]
            measure = meal_data[0][measure_key]
            ingredients.append(f"{measure} {ingredient_name}")

    return ingredients


# dish recipe
@app.route("/dish/<string:id>")
def dish_id(id):
    endpoing = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
    data = requests.get(endpoing)
    dish = data.json()['meals']

    ingredients = get_ingredients(dish)

    return render_template('dish_id.html', dish = dish, ingredients=ingredients)


# search
@app.route("/search", methods=['GET', 'POST'])
def search():
    if (request.method) == 'POST':
        name = request.form.get('dish_name')
        endpoint = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={name}"
        results = requests.get(endpoint)
        data = results.json()['meals']

        return render_template('search.html', data=data, name_form=name)
    


if __name__ == "__main__":
    app.run(debug=True, port=8000)


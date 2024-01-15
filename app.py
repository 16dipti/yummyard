from flask import Flask, render_template, request, abort, redirect, url_for
from model.food import Contact
from db import db
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/food"
db.init_app(app)

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

        post = Contact(
            name=name,
            email=email,
            mobile=mobile,
            message=msg
        )

        db.session.add(post)
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
    
    return render_template('search.html')


    

if __name__ == "__main__":
    app.run(debug=True)


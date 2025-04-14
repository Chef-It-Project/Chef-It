from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home', methods=['GET'])
def home_page():
    # Hard-coded recipes for testing
    recipes = [
    {
        "name": "Classic Pancakes",
        "instructions": "Mix dry ingredients, add wet ingredients, then cook on a buttered griddle until golden.",
        "image": "pancakes.png"
    },
    {
        "name": "Scrambled Eggs",
        "instructions": "Beat eggs, melt butter in a pan, cook eggs while stirring, season with salt and pepper.",
        "image": "eggs.png"
    },
    {
        "name": "Pasta Aglio e Olio",
        "instructions": "Cook pasta; sauté garlic in olive oil; toss together with red pepper flakes and parsley.",
        "image": "pasta.png"
    }
    ]

    # Pass the hard-coded recipes to the template
    return render_template('home.html', recipes=recipes)


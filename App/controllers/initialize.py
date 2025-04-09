from App.database import db
from App.models import User, UserFoodList, Recipe, RecipeIngredient
from werkzeug.security import generate_password_hash

def initialize():
    db.drop_all()
    db.create_all()
    
    # Create test user
    bob = User(username='bob', password='bobpass')
    db.session.add(bob)
    db.session.commit()
    
    # Add inventory items
    inventory_items = [
        'flour', 'sugar', 'eggs', 'milk',
        'butter', 'salt', 'pepper', 'olive oil'
    ]
    for item in inventory_items:
        db.session.add(UserFoodList(bob.id, item))
    
    # Create sample recipes
    recipes = [
        {
            'name': 'Classic Pancakes',
            'ingredients': ['flour', 'eggs', 'milk', 'butter', 'baking powder', 'sugar'],
            'instructions': 'Mix dry ingredients. Add wet ingredients. Cook on buttered griddle.'
        },
        {
            'name': 'Scrambled Eggs',
            'ingredients': ['eggs', 'butter', 'salt', 'pepper'],
            'instructions': 'Beat eggs. Melt butter in pan. Cook eggs while stirring. Season.'
        },
        {
            'name': 'Pasta Aglio e Olio',
            'ingredients': ['pasta', 'garlic', 'olive oil', 'red pepper flakes', 'parsley'],
            'instructions': 'Cook pasta. Sauté garlic in oil. Combine and add seasonings.'
        }
    ]
    
    for recipe_data in recipes:
        recipe = Recipe(
            name=recipe_data['name'],
            instructions=recipe_data['instructions'],
            user_id=bob.id
        )
        db.session.add(recipe)
        db.session.commit()
        
        for ingredient in recipe_data['ingredients']:
            db.session.add(RecipeIngredient(
                recipe_id=recipe.id,
                name=ingredient
            ))
    
    db.session.commit()
    return True
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
    
    # Add inventory items (each record is one unit)
    inventory_items = [
        'flour', 'sugar', 'eggs', 'milk',
        'butter', 'salt', 'pepper', 'olive oil'
    ]
    for item in inventory_items:
        db.session.add(UserFoodList(bob.id, item))
    
    # Create sample recipes with required ingredient quantities
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
        
        # Set required quantities based on the recipe
        if recipe_data['name'] == 'Classic Pancakes':
            quantities = {
                'flour': 1,           # e.g., one bag or unit
                'eggs': 5,
                'milk': 1,
                'butter': 1,
                'baking powder': 1,
                'sugar': 1
            }
        elif recipe_data['name'] == 'Scrambled Eggs':
            quantities = {
                'eggs': 3,
                'butter': 1,
                'salt': 1,
                'pepper': 1
            }
        elif recipe_data['name'] == 'Pasta Aglio e Olio':
            quantities = {
                'pasta': 1,
                'garlic': 2,
                'olive oil': 1,
                'red pepper flakes': 1,
                'parsley': 1
            }
        else:
            # Default to 1 for any unspecified ingredient
            quantities = {ingredient: 1 for ingredient in recipe_data['ingredients']}
        
        for ingredient in recipe_data['ingredients']:
            req_qty = quantities.get(ingredient, 1)
            db.session.add(RecipeIngredient(recipe.id, ingredient, quantity_required=req_qty))
    
    db.session.commit()
    return True
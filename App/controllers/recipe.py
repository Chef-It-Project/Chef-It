from App.models import Recipe, RecipeIngredient, db

def create_recipe(user_id, name, ingredients, instructions):
    recipe = Recipe(name, instructions, user_id)
    db.session.add(recipe)
    db.session.commit()
    
    for ingredient in ingredients:
        db.session.add(RecipeIngredient(
            recipe_id=recipe.id,
            name=ingredient.lower()
        ))
    
    db.session.commit()
    return recipe

def get_recipe_by_id(recipe_id):
    return Recipe.query.get(recipe_id)

def get_user_recipes(user_id):
    return Recipe.query.filter_by(user_id=user_id).all()

def get_user_recipes_json(user_id):
    recipes = get_user_recipes(user_id)
    return [recipe.to_json() for recipe in recipes]

def get_recipes_with_missing_ingredients(user_id):
    from .inventory import get_user_inventory
    
    user_inventory = {i.ingredient for i in get_user_inventory(user_id)}
    recipes = get_user_recipes(user_id)
    result = []
    
    for recipe in recipes:
        missing = []
        for ingredient in recipe.ingredients:
            if ingredient.name not in user_inventory:
                missing.append(ingredient.name)
        
        recipe_data = recipe.to_json()
        recipe_data['missing_ingredients'] = missing
        result.append(recipe_data)
    
    return result
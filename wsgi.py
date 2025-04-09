import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import (
    create_user, get_all_users_json, get_all_users, initialize,
    add_ingredient_to_user, remove_ingredient_from_user, get_user_inventory,
    create_recipe, get_user_recipes, get_recipes_with_missing_ingredients
)

app = create_app()
migrate = get_migrate(app)

# Database initialization
@app.cli.command("init", help="Initialize the database with test data")
def initialize_db():
    initialize()
    print('Database initialized with test user: bob (password: bobpass)')

'''
User Commands Group
'''
user_cli = AppGroup('user', help='User management commands')

@user_cli.command("create", help="Create a new user")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_user_command(username, password):
    user = create_user(username, password)
    if user:
        print(f'User {username} created with ID {user.id}')
    else:
        print(f'User {username} already exists')

@user_cli.command("list", help="List all users")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        users = get_all_users()
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}')
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

'''
Inventory Commands Group
'''
inventory_cli = AppGroup('inventory', help='Inventory management commands')

@inventory_cli.command("add", help="Add ingredient to user's inventory")
@click.argument("user_id", type=int)
@click.argument("ingredient")
def add_ingredient_command(user_id, ingredient):
    if add_ingredient_to_user(user_id, ingredient):
        print(f"Added '{ingredient}' to user {user_id}'s inventory")
    else:
        print("Failed to add ingredient")

@inventory_cli.command("remove", help="Remove ingredient from inventory")
@click.argument("user_id", type=int)
@click.argument("ingredient")
def remove_ingredient_command(user_id, ingredient):
    if remove_ingredient_from_user(user_id, ingredient):
        print(f"Removed '{ingredient}' from user {user_id}'s inventory")
    else:
        print("Failed to remove ingredient")

app.cli.add_command(inventory_cli)

'''
Recipe Commands Group
'''
recipe_cli = AppGroup('recipe', help='Recipe management commands')

@recipe_cli.command("create", help="Create a new recipe")
@click.argument("user_id", type=int)
@click.argument("name")
@click.argument("ingredients")  # Comma-separated
@click.argument("instructions")
def create_recipe_command(user_id, name, ingredients, instructions):
    ingredients_list = [i.strip() for i in ingredients.split(',')]
    recipe = create_recipe(user_id, name, ingredients_list, instructions)
    if recipe:
        print(f"Created recipe '{name}' (ID: {recipe.id})")
    else:
        print("Failed to create recipe")

@recipe_cli.command("missing", help="Show recipes with missing ingredients")
@click.argument("user_id", type=int)
def missing_ingredients_command(user_id):
    recipes = get_recipes_with_missing_ingredients(user_id)
    for recipe in recipes:
        print(f"\n{recipe['name']}:")
        if recipe['missing_ingredients']:
            print("Missing:", ", ".join(recipe['missing_ingredients']))
        else:
            print("All ingredients available")

app.cli.add_command(recipe_cli)

'''
Test Commands Group
'''
test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run user tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("auth", help="Run auth tests")
def auth_tests_command():
    sys.exit(pytest.main(["-k", "AuthTests"]))

app.cli.add_command(test)

if __name__ == '__main__':
    app.run()
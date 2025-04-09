from App.database import db

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, recipe_id, name):
        self.recipe_id = recipe_id
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name
        }
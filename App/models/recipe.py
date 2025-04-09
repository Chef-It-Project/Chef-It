from App.database import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, instructions, user_id):
        self.name = name
        self.instructions = instructions
        self.user_id = user_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'instructions': self.instructions,
            'user_id': self.user_id,
            'ingredients': [ing.to_json() for ing in self.ingredients]
        }
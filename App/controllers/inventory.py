from App.models import UserFoodList, db

def add_ingredient_to_user(user_id, ingredient):
    # Check if already exists
    exists = UserFoodList.query.filter_by(
        user_id=user_id,
        ingredient=ingredient.lower()
    ).first()
    
    if exists:
        return None
    
    new_ingredient = UserFoodList(user_id, ingredient.lower())
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def remove_ingredient_from_user(user_id, ingredient):
    item = UserFoodList.query.filter_by(
        user_id=user_id,
        ingredient=ingredient.lower()
    ).first()
    
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False

def get_user_inventory(user_id):
    return UserFoodList.query.filter_by(user_id=user_id).all()

def get_user_inventory_json(user_id):
    items = get_user_inventory(user_id)
    return [item.to_json() for item in items]
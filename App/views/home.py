from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

home_views = Blueprint('home_views', __name__, template_folder='../templates')

@home_views.route('/home')
@jwt_required()  # Protect this route
def home():
    return render_template('home.html')
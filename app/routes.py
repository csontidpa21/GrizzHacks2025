from flask import Blueprint, jsonify
from .models import User
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Hello from Flask Application Factory!"})

@main.route('/users')
def users():
    users_list = User.query.all()
    return jsonify({
        "users": [{"id": user.id, "username": user.username, "email": user.email} for user in users_list]
    })

@main.route('/add_user/<username>/<email>')
def add_user(username, email):
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "User already exists"}), 400
    
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {username} added!"})

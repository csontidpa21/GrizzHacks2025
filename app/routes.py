from flask import Blueprint
from .models import User
from .extensions import db
from flask import render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')



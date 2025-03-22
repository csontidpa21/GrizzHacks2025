from flask import Blueprint, render_template, redirect, url_for, flash, request

shop = Blueprint('shop', __name__)

@shop.route('/home')
def home():
    '''
    Render
    '''
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
import requests
from .extensions import bcrypt
from .forms import RegistrationForm, LoginForm
from app.controller import create_user, get_user_by_username

auth = Blueprint('auth', __name__)

def get_geoip_location(ip_address):
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        data = response.json()
        if 'loc' in data:
            latitude, longitude = map(float, data['loc'].split(','))
            return latitude, longitude
    except Exception:
        pass
    return None, None

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        latitude, longitude = get_geoip_location(user_ip)

        try:
            user = create_user(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_pw,
                latitude=latitude,
                longitude=longitude
            )
            flash('Account created successfully!', 'success')
            login_user(user)
            return redirect(url_for('shop.home'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('shop.home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
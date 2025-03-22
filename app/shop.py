from flask import Blueprint, render_template, redirect, url_for, flash, request
from .controller import get_paginated_items, get_item_by_id, create_item, delete_item, add_comment
from flask_login import current_user, login_required
shop = Blueprint('shop', __name__)

@shop.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    pagination = get_paginated_items(page=page)
    items = pagination.items
    return render_template('shop/home.html', items=items, pagination=pagination)


@shop.route('/post/<uuid:item_id>')
def post(item_id):
    item = get_item_by_id(item_id)
    return render_template('shop/post.html', item=item)

@shop.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']  # Simplified image handling
        create_item(user_id=current_user.id, name=name, description=description, image_url=image_url)
        flash('Post created!', 'success')
        return redirect(url_for('shop.home'))
    return render_template('shop/new_post.html')

@shop.route('/post/<uuid:item_id>/delete', methods=['POST'])
@login_required
def delete_post(item_id):
    delete_item(item_id)
    flash('Post deleted!', 'success')
    return redirect(url_for('shop.home'))

@shop.route('/post/<uuid:item_id>/comment', methods=['POST'])
@login_required
def comment_post(item_id):
    content = request.form['content']
    add_comment(item_id=item_id, user_id=current_user.id, content=content)
    return redirect(url_for('shop.post', item_id=item_id))

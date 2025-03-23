from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from .controller import (
    get_paginated_items, get_item_by_id, create_item,
    delete_item, add_comment, get_items_by_user,
    get_requested_items, add_requested_item, update_trust_score
)
from .models import ItemConditionEnum

shop = Blueprint('shop', __name__)

@shop.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    pagination = get_paginated_items(page=page)
    items = pagination.items
    return render_template('shop/home.html', items=items, pagination=pagination)


@shop.route('/post/<uuid:item_id>')
@login_required
def post(item_id):
    item = get_item_by_id(item_id)
    return render_template('shop/post.html', item=item)

@shop.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        condition = request.form['condition']
        image_url = request.form.get('image_url', None)

        # Get latitude and longitude from current user for item location
        latitude = current_user.latitude
        longitude = current_user.longitude

        # Ensure the provided condition matches Enum
        try:
            item_condition = ItemConditionEnum[condition]
        except KeyError:
            flash('Invalid condition provided.', 'danger')
            return render_template('shop/new_post.html')

        create_item(
            user_id=current_user.id,
            name=name,
            description=description,
            category=category,
            condition=item_condition,
            latitude=latitude,
            longitude=longitude,
            image_url=image_url
        )
        
        flash('Post created successfully!', 'success')
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


@shop.route('/request-item', methods=['GET', 'POST'])
@login_required
def request_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        add_requested_item(current_user.id, name, description)
        flash('Item request added!', 'success')
        return redirect(url_for('shop.request_queue'))

    return render_template('shop/request_item.html')


@shop.route('/request-queue')
@login_required
def request_queue():
    requests = get_requested_items()
    return render_template('shop/request_queue.html', requests=requests)


@shop.route('/swap/request/<uuid:item_requested_id>', methods=['GET', 'POST'])
@login_required
def request_swap(item_requested_id):
    if request.method == 'POST':
        item_offered_id = request.form['item_offered_id']
        swap_method = request.form['swap_method']
        shipping_address = request.form.get('shipping_address', None)

        request_swap(
            item_requested_id=item_requested_id,
            item_offered_id=item_offered_id,
            swap_method=swap_method,
            shipping_address=shipping_address
        )

        update_trust_score(current_user.id, 5)

        flash('Swap request sent successfully!', 'success')
        return redirect(url_for('shop.home'))

    user_items = get_items_by_user(current_user.id)
    return render_template('shop/request_swap.html', user_items=user_items)

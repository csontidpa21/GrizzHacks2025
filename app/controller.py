from app.extensions import db
from app.models import User, Item, Swap, ItemStatusEnum, SwapStatusEnum
from sqlalchemy import func
# Functions:
# create_user: creates a new user in the database
# get_user_by_username: Queries a user by there username
# update_user_preferences
def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(username, email, password_hash, latitude=None, longitude=None, preferences=None):
    # Check for existing user
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        raise ValueError("User already exists.")

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        latitude=latitude,
        longitude=longitude,
        preferences=preferences or {}
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def update_user_preferences(user_id, preferences):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found.")
    user.set_preferences(preferences)
    db.session.commit()
    return user

def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found.")

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found.")

    db.session.delete(user)
    db.session.commit()
    return True

# ----------------------------
# Geographic Location Queries
# ----------------------------

def get_users_by_location(latitude, longitude, radius_km=10, limit=50):
    """
    Retrieves users within a given radius (in kilometers) from a specified latitude/longitude.
    Uses a simple haversine formula approximation directly in SQL.
    """
    # Earth's radius in kilometers
    EARTH_RADIUS_KM = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat_rad = func.radians(latitude)
    lon_rad = func.radians(longitude)

    # Haversine formula in SQLAlchemy
    distance_expression = EARTH_RADIUS_KM * func.acos(
        func.cos(lat_rad) * func.cos(func.radians(User.latitude)) *
        func.cos(func.radians(User.longitude) - lon_rad) +
        func.sin(lat_rad) * func.sin(func.radians(User.latitude))
    )

    nearby_users = User.query \
        .filter(User.latitude.isnot(None), User.longitude.isnot(None)) \
        .add_columns(distance_expression.label("distance")) \
        .having(distance_expression <= radius_km) \
        .order_by("distance") \
        .limit(limit) \
        .all()

    # Format results nicely
    return [
        {
            "id": user.User.id,
            "username": user.User.username,
            "email": user.User.email,
            "distance_km": round(user.distance, 2),
            "location": user.User.get_location()
        }
        for user in nearby_users
    ]



# ---------------- Item CRUD Operations ----------------
def create_item(user_id, name, description, category, condition, latitude, longitude):
    item = Item(user_id=user_id, name=name, description=description,
                category=category, condition=condition,
                latitude=latitude, longitude=longitude)
    db.session.add(item)
    db.session.commit()
    return item

def get_item_by_id(item_id):
    return Item.query.get(item_id)

def update_item(item_id, **kwargs):
    item = get_item_by_id(item_id)
    if not item:
        raise ValueError("Item not found.")
    for key, value in kwargs.items():
        if hasattr(item, key):
            setattr(item, key, value)
    db.session.commit()
    return item

def delete_item(item_id):
    item = get_item_by_id(item_id)
    if not item:
        raise ValueError("Item not found.")
    db.session.delete(item)
    db.session.commit()
    return True

# ---------------- Swap CRUD Operations ----------------
def request_swap(item_requested_id, item_offered_id):
    swap = Swap(item_requested_id=item_requested_id,
                item_offered_id=item_offered_id,
                status=SwapStatusEnum.PENDING)
    db.session.add(swap)
    db.session.commit()
    return swap

def respond_to_swap(swap_id, status):
    swap = Swap.query.get(swap_id)
    if swap:
        swap.status = status
        db.session.commit()
    return swap

# ---------------- Queries & Filtering ----------------
def get_all_items(status='Available', limit=100):
    return Item.query.filter_by(status=status).limit(limit).all()

def get_items_by_user(user_id, limit=50):
    return Item.query.filter_by(user_id=user_id).limit(limit).all()

def get_items_by_location(latitude, longitude, radius_km=10, limit=50):
    EARTH_RADIUS_KM = 6371.0
    lat_rad = func.radians(latitude)
    lon_rad = func.radians(longitude)

    distance_expression = EARTH_RADIUS_KM * func.acos(
        func.cos(lat_rad) * func.cos(func.radians(Item.latitude)) *
        func.cos(func.radians(Item.longitude) - lon_rad) +
        func.sin(lat_rad) * func.sin(func.radians(Item.latitude))
    )

    nearby_items = Item.query \
        .filter(Item.latitude.isnot(None), Item.longitude.isnot(None)) \
        .add_columns(distance_expression.label("distance")) \
        .having(distance_expression <= radius_km) \
        .order_by("distance") \
        .limit(limit).all()

    return [
        {
            "id": item.Item.id,
            "name": item.Item.name,
            "description": item.Item.description,
            "distance_km": round(item.distance, 2),
            "location": {"latitude": item.Item.latitude, "longitude": item.Item.longitude},
            "condition": item.Item.condition.value,
            "status": item.Item.status.value
        }
        for item in nearby_items
    ]

def get_swaps_by_user(user_id, limit=50):
    return Swap.query.join(Item, Swap.item_requested_id == Item.id) \
        .filter(Item.user_id == user_id) \
        .limit(limit).all()

def complete_swap(swap_id):
    swap = Swap.query.get(swap_id)
    if not swap:
        raise ValueError("Swap not found.")
    swap.status = SwapStatusEnum.COMPLETED
    swap.item_requested.status = ItemStatusEnum.SWAPPED
    swap.item_offered.status = ItemStatusEnum.SWAPPED

    swap.item_requested.owner.gamification_points += 10
    swap.item_offered.owner.gamification_points += 10

    db.session.commit()
    return swap

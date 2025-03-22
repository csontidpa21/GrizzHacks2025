from app.extensions import db
from app.models import User
from sqlalchemy import func
# Functions:
# create_user: creates a new user in the database
# get_user_by_username: Queries a user by there username
# update_user_preferences
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


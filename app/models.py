from .extensions import db, login_manager
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # Columns (Data attributes)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    preferences = db.Column(JSONB, nullable=True)
    gamification_points = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Representation (useful for debugging)
    def __repr__(self):
        return f'<User {self.username}>'

    # Helper methods (Simple logic for single-instance manipulation)
    def set_location(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_location(self):
        return {"latitude": self.latitude, "longitude": self.longitude}

    def set_preferences(self, preferences: dict):
        self.preferences = preferences

    def get_preferences(self):
        return self.preferences

    

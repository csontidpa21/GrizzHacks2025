from .extensions import db, login_manager
from sqlalchemy import func, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from flask_login import UserMixin
import enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    preferences = db.Column(JSONB, nullable=True)
    gamification_points = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    items = db.relationship('Item', backref='owner', lazy='dynamic')

class ItemConditionEnum(enum.Enum):
    NEW = 'New'
    LIKE_NEW = 'Like New'
    USED = 'Used'
    DAMAGED = 'Damaged'

class ItemStatusEnum(enum.Enum):
    AVAILABLE = 'Available'
    RESERVED = 'Reserved'
    SWAPPED = 'Swapped'

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    condition = db.Column(Enum(ItemConditionEnum), nullable=False, default=ItemConditionEnum.USED)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    status = db.Column(Enum(ItemStatusEnum), default=ItemStatusEnum.AVAILABLE, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

class SwapStatusEnum(enum.Enum):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

class Swap(db.Model):
    __tablename__ = 'swaps'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_requested_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), nullable=False)
    item_offered_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), nullable=False)
    status = db.Column(Enum(SwapStatusEnum), default=SwapStatusEnum.PENDING, nullable=False)
    initiated_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    item_requested = db.relationship('Item', foreign_keys=[item_requested_id])
    item_offered = db.relationship('Item', foreign_keys=[item_offered_id])

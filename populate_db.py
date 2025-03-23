from app import create_app
from app.extensions import db, bcrypt
from app.models import User, Item, Comment, ItemConditionEnum, ItemStatusEnum
import uuid
import random

app = create_app()

def create_sample_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(
        id=uuid.uuid4(),
        username='user',
        email='testuser@example.com',
        password_hash=password_hash,
        latitude=42.3314,
        longitude=-83.0458,
        gamification_points=50
    )
    db.session.add(user)
    return user

def create_sample_items(user):
    items = []
    sample_items = [
        {
            'name': 'iPhone Charger',
            'description': 'A brand-new iPhone charger.',
            'category': 'Electronics',
            'condition': ItemConditionEnum.NEW,
            'status': ItemStatusEnum.AVAILABLE,
            'image_url': 'https://img.casebus.com/upload/product/90064/90064/35W-Type-C-Charger-1.jpg'
        },
        {
            'name': 'Mountain Bike',
            'description': 'A lightly used mountain bike.',
            'category': 'Sports',
            'condition': ItemConditionEnum.LIKE_NEW,
            'status': ItemStatusEnum.AVAILABLE,
            'image_url': 'https://i5.walmartimages.com/asr/3e93bdb8-f247-4ae2-898a-e03fe12a5472.c6b499258d504157384035a890ee022e.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF'
        },
        {
            'name': 'Vintage Guitar',
            'description': 'Classic acoustic guitar from 1980s.',
            'category': 'Music',
            'condition': ItemConditionEnum.USED,
            'status': ItemStatusEnum.RESERVED,
            'image_url': 'https://cdn.mos.cms.futurecdn.net/xUmiWSrVN5RSjRw3htM5rL.jpg'
        },
    ]

    for item_data in sample_items:
        item = Item(
            id=uuid.uuid4(),
            user_id=user.id,
            name=item_data['name'],
            description=item_data['description'],
            category=item_data['category'],
            condition=item_data['condition'],
            status=item_data['status'],
            image_url=item_data['image_url'],
            latitude=user.latitude + random.uniform(-0.01, 0.01),
            longitude=user.longitude + random.uniform(-0.01, 0.01)
        )
        db.session.add(item)
        items.append(item)
    return items

def create_sample_comments(items, user):
    sample_comments = [
        'Is this still available?',
        'Could we meet tomorrow?',
        'Great item, very interested!',
    ]

    for item in items:
        comment = Comment(
            id=uuid.uuid4(),
            item_id=item.id,
            user_id=user.id,
            content=random.choice(sample_comments)
        )
        db.session.add(comment)

def populate_db():
    with app.app_context():
        print("Dropping existing tables and creating new ones...")
        db.drop_all()
        db.create_all()

        print("Creating sample user...")
        user = create_sample_user()

        print("Creating sample items...")
        items = create_sample_items(user)

        print("Creating sample comments...")
        create_sample_comments(items, user)

        db.session.commit()
        print("Database populated successfully.")

if __name__ == '__main__':
    populate_db()

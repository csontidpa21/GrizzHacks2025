# EcoSwap

A gamified trading platform built with Flask, SQLAlchemy, and PostgreSQL (SQLite for development). This platform enables users to trade items securely, leverage geo-location features, and enjoy an engaging user experience.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Setup](#setup)
- [Database](#database)
- [Running the Application](#running-the-application)
- [Structure](#structure)
- [Routes and Endpoints](#routes-and-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
EcoSwap is designed to make item trading simple, engaging, and secure. Users can list items, comment on posts, request item swaps, and accumulate points through active participation.

---

## Key Features
- **User Authentication**: Secure account registration and login
- **Item Listings**: Users can list items with detailed descriptions, conditions, and images
- **Comments and Engagement**: Interactive commenting system for item listings
- **Gamification**: Users earn points through successful interactions and trades
- **Geo-location**: Automatically detect and display nearby items and traders
- **Pagination**: Efficient navigation for item listings

---

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **Security**: Password hashing with bcrypt, secure session management

---

## Setup

### Prerequisites
- Python 3.11+

### Installation

Clone the repository:
```sh
git clone https://github.com/<username>/EcoSwap.git
cd EcoSwap
```

Create and activate virtual environment:
```sh
python3 -m venv env
source env/bin/activate
```

Install dependencies:
```sh
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file in the project root:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/ecoswap_db
```

---

## Database

### Initialize Database

Use provided script:
```sh
python populate_db.py
```

Or manually via Flask-Migrate:
```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## Running the Application

Start development server:
```sh
python run.py
```

Access application at `http://localhost:5000`.

---

## Structure

```
EcoSwap/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── controller.py
│   ├── extensions.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── shop.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── shop/
│       ├── base.html
│       └── index.html
├── config.py
├── populate_db.py
├── run.py
└── requirements.txt
```

---

## Routes and Endpoints

- **Auth**:
  - `/auth/register`
  - `/auth/login`
  - `/auth/logout`

- **Shop**:
  - `/shop/home`
  - `/shop/post/<item_id>`
  - `/shop/post/new`
  - `/shop/post/<item_id>/delete`
  - `/shop/post/<item_id>/comment`

- **Main**:
  - `/`

---

## Contributing
1. Fork repository
2. Create branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Create Pull Request

---

## License
MIT License

© 2025 EcoSwap

# GrizzHacks2025

## Hackathon at Oakland University

Hi


### Files
- `app/__init__.py`: Application factory for instantiating flask application
- `app/forms.py`: Forms for use in the Web Application
- `app/static`: Contains all `js` scripts, images under `img`, and CSS styling under `css`
- `config.py`: Contains all configuration information
- `run.py`: This runs the flask application (`python run.py`)
- `app/models.py`: Contains the database schema definition and some getter/setter functions
- `app/extensions.py`: Instantiates some libraries to avoid circular imports
- `app/controller.py`: Contains all the functions to interface with the database (create users, deleted users etc). CRUD operations
- `app/auth.py`: This contains the `/auth` blueprint for handling user registration/authentication etc.
- `app/templates/*`: Contains all HTML templates/files
- `app/shop.py`: Contains functionality for controlling the web shop.

To install packages:
```bash
git clone ....
pip install -r requirements.txt
```

Run

```bash
python run.py
```

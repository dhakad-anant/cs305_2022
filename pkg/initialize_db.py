from flask import Flask
from pkg.Database import Database

# Creating a Flask app
app = Flask(__name__)

db = Database(app)

with app.app_context():
    db.create_table()

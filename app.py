from flask import Flask
from models import db
from routes import app

with app.app_context():
    db.create_all()
    print("Database initialized successfully!")

if __name__ == "__main__":
    app.run(debug=True)

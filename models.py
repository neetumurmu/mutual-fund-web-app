from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    portfolio = db.relationship("Portfolio", backref="user", lazy=True)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fund_family = db.Column(db.String(120), nullable=False)
    fund_name = db.Column(db.String(120), nullable=False)
    units = db.Column(db.Float, nullable=False)
    investment_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

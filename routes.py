from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from models import db, User, Portfolio
from utils import fetch_mutual_funds, create_token
from werkzeug.security import generate_password_hash, check_password_hash
from constants import fund_families

app = Flask(__name__)
app.config.from_object("config.Config")

jwt = JWTManager(app)
db.init_app(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "Server is up and running"}), 200


# Registration Route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print("data: ", data)
    email = data.get("email")
    password = data.get("password")
    hashed_password = generate_password_hash(password)

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


# Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_token(str(user.id))
    return jsonify({"message": "Login successful", "token": token})


# Fetch Mutual Funds
@app.route("/funds", methods=["GET"])
@jwt_required()
def get_funds():
    fund_family = request.args.get("fund_family")
    if not fund_family:
        return jsonify({"message": "Fund family is required"}), 400

    funds = fetch_mutual_funds(fund_family)
    return jsonify(funds)


# Add Investment to Portfolio
@app.route("/api/v1/portfolio/funds", methods=["POST"])
@jwt_required()
def add_fund_to_portfolio():
    data = request.get_json()

    required_fields = ["fund_family", "fund_name", "units", "investment_value"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    fund_family = data["fund_family"]
    fund_name = data["fund_name"]
    units = data["units"]
    investment_value = data["investment_value"]

    user_id = get_jwt_identity()

    new_portfolio = Portfolio(
        fund_family=fund_family,
        fund_name=fund_name,
        units=units,
        investment_value=investment_value,
        user_id=user_id,
    )

    db.session.add(new_portfolio)
    db.session.commit()
    return jsonify({"message": "Investment added to portfolio!"}), 201


# View Portfolio
@app.route("/api/v1/portfolio", methods=["GET"])
@jwt_required()
def view_portfolio():
    user_id = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=user_id).all()

    if not portfolio:
        return jsonify({"message": "No portfolio found for this user."}), 404

    portfolio_data = [
        {
            "fund_family": p.fund_family,
            "fund_name": p.fund_name,
            "units": p.units,
            "investment_value": p.investment_value,
        }
        for p in portfolio
    ]

    return jsonify(portfolio_data), 200


# Track Portfolio Value (Hourly)
@app.route("/track", methods=["GET"])
@jwt_required()
def track_portfolio():
    user_id = get_jwt_identity()
    portfolio = Portfolio.query.filter_by(user_id=user_id).all()

    updated_values = []
    for p in portfolio:
        fund_data = fetch_mutual_funds(p.fund_family)
        # Logic to calculate the updated value based on the current price
        updated_value = p.units * fund_data["current_price"]
        updated_values.append(
            {"fund_name": p.fund_name, "updated_value": updated_value}
        )

    return jsonify(updated_values)

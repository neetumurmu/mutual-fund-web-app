import requests
from flask_jwt_extended import create_access_token
from config import Config
from datetime import timedelta


def fetch_mutual_funds(fund_family):
    url = Config.RAPIDAPI_URL

    querystring = {"Mutual_Fund_Family": fund_family, "Scheme_Type": "Open"}

    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": Config.RAPIDAPI_HOST,
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def create_token(user_id):
    return create_access_token(identity=user_id, expires_delta=timedelta(hours=1))

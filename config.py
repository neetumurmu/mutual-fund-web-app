import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RAPIDAPI_URL = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
    RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
    RAPIDAPI_HOST = os.environ["RAPIDAPI_HOST"]

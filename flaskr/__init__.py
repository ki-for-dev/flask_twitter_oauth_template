from enum import unique
from operator import truediv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

import os

from datetime import datetime
import pytz 

print(__name__)

app = Flask(__name__, static_folder='-')

# DB接続設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': 'root',
    'password': 'password',
    'host': 'db:3306',
    'db_name': 'appdb'
})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

#
# Models
#
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Twitter内部の固有ID
    tw_id = db.Column(db.String(128), nullable=False, unique=True)
    # アットマークID
    tw_screen_id = db.Column(db.String(128), nullable=False, unique=False)
    # 名前
    tw_name = db.Column(db.String(128), nullable=False, unique=False)
    # プロフィール
    tw_description = db.Column(db.String(128), nullable=True)
    # 鍵垢
    tw_protected = db.Column(db.Boolean, nullable=False)
    # アイコン画像
    tw_profile_image_url = db.Column(db.String(128), nullable=True)
    # トークン
    tw_access_token = db.Column(db.String(128), nullable=True)
    tw_access_token_secret = db.Column(db.String(128), nullable=True)

    #
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')), onupdate=datetime.now())

    def search_by_id(id):
        return db.session.query(User).filter(User.id == id).first()

    def search_by_tw_id(tw_id):
        return db.session.query(User).filter(User.tw_id == tw_id).first()

    def search_by_tw_screen_id(tw_screen_id):
        return db.session.query(User).filter(User.tw_screen_id == tw_screen_id).order_by(User.updated_at).first()

# LoginManager初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'twitter_login'
import flaskr.main

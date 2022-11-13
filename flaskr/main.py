from os import access
from threading import currentThread
from flaskr import app
from flask import render_template, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
import traceback

# from werkzeug.security import generate_password_hash, check_password_hash

from . import User
from . import db
from . import login_manager
# from .auth import oauth_twitter_oauth2 as oauth_twitter
from .oauth import oauth_twitter_oauth1session as oauth_twitter

@app.route('/')
def home():
    return render_template('views/index.html')

# Twitter認証

# 「Twitterでログイン」ボタンから遷移
# Twitter認証画面へリダイレクト
@app.route('/twitter-login', methods=['GET'])
def twitter_login():
    oauth_url = oauth_twitter.create_authorization_url()
    return redirect(oauth_url)

# Twitter認証画面からコールバック
@app.route('/twitter-callback')
def twitter_callback():
    oauth_denied = request.args.get('denied')
    if oauth_denied:
        # 認証失敗
        return redirect('/?login-failed=1')
    # 認証成功
    access_token_content = oauth_twitter.fetch_access_token_content(request.url)
    
    # 認証したユーザーでログイン
    # 未登録なら登録
    user_profile = oauth_twitter.fetch_profile_by_id(access_token_content['user_id']).json()
    user = User.query.filter_by(tw_id=user_profile['data']['id']).first()
    if user == None:
        # ユーザー登録
        user = User(
            tw_id=user_profile['data']['id'],
            tw_screen_id=user_profile['data']['username'],
            tw_name=user_profile['data']['name'],
            tw_description=user_profile['data']['description'],
            tw_protected=user_profile['data']['protected'],
            tw_profile_image_url=user_profile['data']['profile_image_url'],
            tw_access_token=access_token_content['oauth_token'],
            tw_access_token_secret=access_token_content['oauth_token_secret']
        )
        db.session.add(user)
        db.session.commit()
    else:
        # ユーザー情報更新
        user.tw_screen_id = user_profile['data']['username']
        user.tw_name = user_profile['data']['name']
        user.tw_description = user_profile['data']['description']
        user.tw_protected = user_profile['data']['protected']
        user.tw_profile_image_url = user_profile['data']['profile_image_url']
        user.tw_access_token = access_token_content['oauth_token']
        user.tw_access_token_secret = access_token_content['oauth_token_secret']
        db.session.add(user)
        db.session.commit()
    login_user(user)
    # プロフィール作成ページにリダイレクト
    return redirect('/home')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/home', methods=['GET'])
@login_required
def user_home():
    """
    ユーザーのホーム画面を表示
    """
    print('@update')
    return render_template('views/user_home.html')

@login_manager.user_loader
def load_user(user_id):
    """
    セッションからログインユーザーを特定する
    """
    return User.query.get(int(user_id))
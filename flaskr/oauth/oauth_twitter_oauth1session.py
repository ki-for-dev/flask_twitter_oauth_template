import os
import sys
import traceback

from requests_oauthlib import OAuth1Session

from .oauth_config import twitter 
from requests import Response

AccessTokenData = dict[
    'oauth_token': str,
    'oauth_token_secret': str,
    'user_id': str,
    'screen_name': str,
]

UserProfileData = dict[
    'data': dict[
        'id': str,
        'username': str,
        'name': str,
        'profile_image_url': str,
        'description': str,
        'protected': bool,
    ]
]

host = 'https://api.twitter.com'
oauth_session: OAuth1Session = None

def create_oauth_session(api_key, api_key_secret, access_token, access_token_secret) -> None:
    global oauth_session
    oauth_session = OAuth1Session(
        client_key=api_key,
        client_secret=api_key_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )

def create_authorization_url() -> str:
    print(os.environ.get('TWITTER_API_KEY'))
    print(sys._getframe().f_code.co_name)
    """
    Twitterの認証画面のURLを生成する。
    """
    oauth_session = OAuth1Session(
        client_key=twitter.API_KEY,
        client_secret=twitter.API_KEY_SECRET,
        callback_uri=twitter.CALLBACK_URL
    )
    # リクエストトークンを要求
    oauth_session.fetch_request_token(twitter.REQUESET_TOKEN_URL)
    # リクエストトークンから認証画面URLを生成
    redirect_url = oauth_session.authorization_url(twitter.AUTHORIZATION_URL)
    return redirect_url

def fetch_access_token_content(redirect_response) -> AccessTokenData:
    print(sys._getframe().f_code.co_name)
    """
    Twitter認証画面で認証後、リダイレクトされてきたURLを使ってアクセストークンを取得する。

    Parameters:
    - redirect_response: リダイレクトされてきたURL

    Returns:
    {
        'oauth_token': アクセストークン,
        'oauth_token_secret': アクセストークンシークレット,
        'user_id': Twitter固有ID,
        'screen_name': Twitter表示ID
    }
      
    Examples:
    ```python
        fetch_access_token(request.url)
    ```
    """
    # oauth_session作成
    _oauth_session = OAuth1Session(
      client_key=twitter.API_KEY,
      client_secret=twitter.API_KEY_SECRET,
    )
    _oauth_session.parse_authorization_response(redirect_response)
    # リクエストトークン取得、セット
    content = _oauth_session.fetch_access_token(twitter.ACCESS_TOKEN_URL)
    # グローバル変数のoauth_sessionを更新
    global oauth_session
    oauth_session = _oauth_session
    return content

def fetch_profile_by_id(tw_id: str) -> Response:
    print(sys._getframe().f_code.co_name)
    """
    Twitterのプロフィールを取得する。
    """
    try:
        res = oauth_session.get(
            host + '/2/users/' + tw_id,
            params={
                'user.fields': ','.join([
                    'description',
                    'profile_image_url',
                    'protected'
                ])
            }
        )
        return res
    except:
        raise



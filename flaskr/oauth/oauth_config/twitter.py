import os

API_KEY = os.environ.get('TWITTER_API_KEY')
API_KEY_SECRET = os.environ.get('TWITTER_API_KEY_SECRET')
CALLBACK_URL = os.environ.get('TWITTER_CALLBACK')

REQUESET_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHENTICATE_URL = 'https://api.twitter.com/oauth/authenticate'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'


import base64
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from django.conf import settings


def generate_access_token(consumer_key=None, consumer_secret=None):
    """Generate M-Pesa access token"""
    consumer_key = consumer_key or settings.MPESA_CONSUMER_KEY
    consumer_secret = consumer_secret or settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    return None


def lipa_na_mpesa_online(access_token, business_short_code, lipa_na_mpesa_online_passkey, 
                         amount, phone_number, callback_url, account_reference, transaction_desc):
    """Initiate M-Pesa STK Push"""
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": business_short_code,
        "Password": online_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(amount),
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def get_movie_data(imdb_id):
    """Get movie data from OMDB API"""
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def search_movies(query):
    """Search movies using OMDB API"""
    url = f'http://www.omdbapi.com/?s={query}&apikey={settings.OMDB_API_KEY}&type=movie'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Search', [])
    return []

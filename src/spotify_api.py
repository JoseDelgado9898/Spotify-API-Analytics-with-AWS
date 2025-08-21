import requests
import os
import json
from dotenv import load_dotenv
from datetime import date
from S3_wrapper import S3_Client


def generate_bearer():
    body_data = {
        "grant_type":"client_credentials",
        "client_id":os.getenv('SPOTIFY_CLIENT_ID'),
        "client_secret":os.getenv('SPOTIFY_CLIENT_SECRET')
    }
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data = body_data,
        verify=False
     )
    access_token = response.json()['access_token']
    return access_token

def get_artist(artist_id,token):
    headers = {"Authorization":f"Bearer {token}"}
    base_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(
        base_url,
        headers=headers,
        verify=False
    )
    return response.json()

def get_artists_top_tracks(artist_id,token):
    headers = {"Authorization":f"Bearer {token}"}
    query_params = {
        "market":"ES"
    }
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers=headers,
        verify=False,
        params=query_params)
    return response.json()

def get_artists_albums(artist_id,token):
    headers = {"Authorization":f"Bearer {token}"}
    base_url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    query_params = {
        "market":"ES"
    }
    response = requests.get(
        base_url,
        headers=headers,
        verify=False,
        params=query_params
    )
    return response.json()


if __name__=='__main__':
    load_dotenv()
    current_date = date.today()
    token = generate_bearer()
    print(token)
    s3_client= S3_Client()
    artist_ids = [
    "4YRxDV8wJFPHPTeXepOstw", "06HL4z0CvFAxyc27GXpf02", "6eUKZXaKkcviH0Ku9w2n3V",
    "6qqNVTkY8uBg9cP3Jd7DAH", "1Xyo4u8uXC1ZmMpatF05PJ", "66CXWjxzNUsdJxJ2JdwvnR",
    "7dGJo4pcD2V6oG8kP0tJRR", "3TVXtAsR1Inumwj472S9r4", "4q3ewBCX7sLwd24euuV69X",
    "1uNFoZAHBGtllmzznpCI3s", "3Nrfpe0tUJi4K4DXYWgMUX", "0du5cEVh5yTK9QJze8zA0C",
    "5pKCCKE2ajJHZ9KAiaK11H", "1mYsTxnqsietFxj1OgoGbG", "4dpARuHxo51G3z768sgnrY",
    "4gzpq5DPGxSnKTe4SA8HAU", "790FomKkXshlbRYZFtlgla", "53XhwfbYqKCa1cC15pYq2q",
    "1wRPtKGflJrBx9BmLsSwlU", "41MozSoPIsD1dJM0CLPjZF"
]
    for id in artist_ids:
        data = get_artist(id,token)
        print(data)
        key=f'{date.today()}/{data['name']}'
        #s3_client.upload_object(data,'spotify-s3-poc',key)


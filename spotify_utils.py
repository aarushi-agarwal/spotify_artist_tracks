#spotify_utils.py
#When using flask_app.py, load from .env file 
#from dotenv import load_dotenv
#import os
#load_dotenv()
#client_id = os.getenv("CLIENT_ID")
#client_secret = os.getenv("CLIENT_SECRET")

import streamlit as st
import base64
from requests import post, get
import json

client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
    
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
 
# Function to return the artist_id on searching by artist name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query 
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artists with this name exist...Booooo")
        return None
    
    artist_data = json_result[0]
    artist_info = {
        "id": artist_data["id"],
        "name": artist_data["name"]
    }
    return artist_info
    

# Get the album_ids by an artist_id
def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    album_ids = {album["id"] for album in json_result}  # Use a set to avoid duplicate album IDs
    return album_ids

# Get the tracks from an album_id
def get_tracks_from_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

# Get all the tracks by an artist_id
def get_all_tracks_by_artist(token, artist_id):
    album_ids = get_albums_by_artist(token, artist_id)
    all_tracks = []
    for album_id in album_ids:
        tracks = get_tracks_from_album(token, album_id)
        all_tracks.extend(tracks)  # Add all tracks from this album
    return all_tracks

# Get the top tracks by an artist_id
def get_top_tracks_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result  

def calculate_total_listening_time(tracks):
    total_duration_ms = sum(track['duration_ms'] for track in tracks)
    total_duration_s = total_duration_ms / 1000  # convert milliseconds to seconds
    hours, remainder = divmod(total_duration_s, 3600)  # get hours and remainder in seconds
    minutes, seconds = divmod(remainder, 60)  # get minutes and seconds
    return int(hours), int(minutes), int(seconds)


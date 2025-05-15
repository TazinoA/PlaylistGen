from datetime import timedelta
from flask import Flask, url_for, render_template, session, redirect, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
import scrape

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("app_secret")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

def get_sp():
    load_dotenv()
    sp_oauth = SpotifyOAuth(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"),
                            redirect_uri=url_for("redirect_page", _external=True),
                            scope="playlist-read-private playlist-modify-public playlist-modify-private playlist-read-collaborative ugc-image-upload user-top-read")
    return sp_oauth

@app.route("/")
def get_auth():
    return redirect(get_sp().get_authorize_url())


@app.route("/redirect")
def redirect_page():
    session.permanent = True
    session.clear()
    code = request.args["code"]
    token_info = get_sp().get_access_token(code)

    session["token_info"] = token_info
    session['expires_in'] = token_info['expires_in']
    session['start_time'] = time.time()
    return redirect(url_for("get_billboard_date", _external=True))

@app.route("/search", methods=["POST", "GET"])
def get_billboard_date():
    query = request.form.get("query")
    if query:
        session["date"] = query
        return redirect("http://127.0.0.1:5000/playlist")
    return render_template("index.html", query=query)

def get_client():
    token_info = session.get("token_info")
    if not token_info:
        return redirect(url_for("get_auth"))
    expiration_time = session['start_time'] + session['expires_in']

    if time.time() > expiration_time:
        sp_oauth = get_sp()
        refresh_token = token_info["refresh_token"]
        token_info = sp_oauth.refresh_access_token(refresh_token)
        session["token_info"] = token_info
        session['start_time'] = time.time()


    return spotipy.Spotify(auth = token_info["access_token"])


def get_song_uri(song):
    sp = get_client()
    response = sp.search(song, limit = 1, type = "track")
    return response["tracks"]["items"][0]["uri"]

def create_playlist(date):
    sp = get_client()
    id = sp.current_user()["id"]
    name = f"Billboard Hot 100 {date}"
    playlist = sp.user_playlist_create(user = id, name = name, public = False, description = "Created in python")
    return playlist["id"]

def add_songs(playlist_id, tracks):
    sp = get_client()
    sp.playlist_add_items(playlist_id=playlist_id, items=tracks)



@app.route("/playlist")
def process_playlist():
    date = session["date"]
    songs = scrape.get_billboard_data(date)
    if songs:
        song_uris = [get_song_uri(song) for song in songs]
        playlist_id = create_playlist(date)
        add_songs(playlist_id=playlist_id, tracks=song_uris)
        return "<h1>Success! You can view the playlist in your spotify library</h1>"
    else:
        return "Date should be in format YYYY-MM-DD, Please go back and search for a date"


if __name__ == "__main__":
    app.run(debug=True)


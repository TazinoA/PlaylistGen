# Billboard to Spotify Playlist Creator

## Description
This application scrapes the Billboard Hot 100 chart for a given date and creates a Spotify playlist of the songs.

## Features
*   Fetches top 100 songs from Billboard for a user-specified date.
*   Authenticates with the user's Spotify account using OAuth.
*   Creates a new private playlist in the user's Spotify library, named "Billboard Hot 100 [YYYY-MM-DD]".
*   Adds the fetched songs to this new playlist.

## Setup and Installation

### Prerequisites
*   Python 3.x
*   pip

### Instructions
1.  Clone the repository: `git clone <repository_url>`
2.  Navigate to the project directory: `cd <project_directory>`
3.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  Install dependencies: `pip install -r requirements.txt` (Note: `requirements.txt` will be created in a later step).
5.  Create a `.env` file in the root of the project directory with your Spotify API credentials and a Flask secret key:
    ```env
    CLIENT_ID='YOUR_SPOTIFY_CLIENT_ID'
    CLIENT_SECRET='YOUR_SPOTIFY_CLIENT_SECRET'
    app_secret='YOUR_FLASK_APP_SECRET_KEY'
    ```
    (`app_secret` can be any random strong string. It is used by Flask to sign session cookies and other security-sensitive data.)

## Usage
1.  Run the Flask application: `python spotify.py`
2.  Open your web browser and go to `http://127.0.0.1:5000/`.
3.  You will be redirected to Spotify for authentication.
4.  After authentication, you will be redirected to a page where you can enter a date (format YYYY-MM-DD).
5.  Upon submission, a playlist named "Billboard Hot 100 YYYY-MM-DD" will be created in your Spotify account.

## Dependencies
*   Flask
*   Spotipy
*   Requests
*   Beautiful Soup 4
*   python-dotenv


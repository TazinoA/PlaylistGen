import requests
from bs4 import BeautifulSoup


def get_billboard_data(date):
    url = f"https://billboard.com/charts/hot-100/{date}"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
    response = requests.get(url, headers=header)

    if response.status_code != 200:
        return None
    web_page = response.text

    soup = BeautifulSoup(web_page, "html.parser")

    song_spans = soup.select("li ul li h3")

    songs = [song.getText().strip() for song in song_spans]
    return songs

import requests
import os
from datetime import datetime

# Use environment variables directly (GitHub Actions will set these)
TRAKT_CLIENT_ID = os.environ['TRAKT_CLIENT_ID']
TRAKT_ACCESS_TOKEN = os.environ['TRAKT_ACCESS_TOKEN']
TMDB_ACCESS_TOKEN = os.environ['TMDB_ACCESS_TOKEN']


# API endpoints
TRAKT_TV_ENDPOINT = 'https://api.trakt.tv/users/me/history/shows'
TRAKT_MOVIE_ENDPOINT = 'https://api.trakt.tv/users/me/history/movies'
TMDB_TV_URL = 'https://api.themoviedb.org/3/tv/'
TMDB_MOVIE_URL = 'https://api.themoviedb.org/3/movie/'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w200'  # Using width 200px images

# Headers
trakt_headers = {
    'Content-Type': 'application/json',
    'trakt-api-version': '2',
    'trakt-api-key': TRAKT_CLIENT_ID,
    'Authorization': f'Bearer {TRAKT_ACCESS_TOKEN}'
}

tmdb_headers = {
    'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
    'accept': 'application/json'
}

def fetch_last_watched(endpoint):
    response = requests.get(endpoint, headers=trakt_headers)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_tmdb_image(tmdb_id, media_type):
    if media_type == 'tv':
        url = f"{TMDB_TV_URL}{tmdb_id}"
    else:
        url = f"{TMDB_MOVIE_URL}{tmdb_id}"
    
    response = requests.get(url, headers=tmdb_headers)
    
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
    return None

# Fetch last watched TV show and movie
last_show = fetch_last_watched(TRAKT_TV_ENDPOINT)
last_movie = fetch_last_watched(TRAKT_MOVIE_ENDPOINT)


jekyll_content = """---
layout: none
---

<div class="trakt-embed">
    <h3>Last Watched on Trakt</h3>
"""

if last_show:
    show = last_show['show']
    episode = last_show['episode']
    watched_at = datetime.fromisoformat(last_show['watched_at'].replace('Z', '+00:00'))
    image_url = get_tmdb_image(show['ids']['tmdb'], 'tv')
    jekyll_content += f"""
    <div class="item">
        <img class="item-image" src="{image_url or '/path/to/default/image.jpg'}" alt="{show['title']}">
        <div class="item-details">
            <p><strong>TV Show:</strong> {show['title']}</p>
            <p><strong>Episode:</strong> {episode['title']} (S{episode['season']:02d}E{episode['number']:02d})</p>
            <p class="timestamp">Watched: {watched_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
    """

if last_movie:
    movie = last_movie['movie']
    watched_at = datetime.fromisoformat(last_movie['watched_at'].replace('Z', '+00:00'))
    image_url = get_tmdb_image(movie['ids']['tmdb'], 'movie')
    jekyll_content += f"""
    <div class="item">
        <img class="item-image" src="{image_url or '/path/to/default/image.jpg'}" alt="{movie['title']}">
        <div class="item-details">
            <p><strong>Movie:</strong> {movie['title']} ({movie['year']})</p>
            <p class="timestamp">Watched: {watched_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
    """

jekyll_content += "</div>"

# Save Jekyll-friendly content
with open('_includes/trakt_embed.html', 'w') as f:
    f.write(jekyll_content)

print("Jekyll include file generated and saved as '_includes/trakt_embed.html'")
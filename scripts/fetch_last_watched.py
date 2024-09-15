import requests
import os
from datetime import datetime
import sys



# Redirect stderr to a file
sys.stderr = open('error_log.txt', 'w')

print("Checking environment variables:")
print(f"TRAKT_CLIENT_ID: {'Set' if 'TRAKT_CLIENT_ID' in os.environ else 'Not set'}")
print(f"TRAKT_CLIENT_SECRET: {'Set' if 'TRAKT_CLIENT_SECRET' in os.environ else 'Not set'}")
print(f"TRAKT_REFRESH_TOKEN: {'Set' if 'TRAKT_REFRESH_TOKEN' in os.environ else 'Not set'}")
print(f"TMDB_ACCESS_TOKEN: {'Set' if 'TMDB_ACCESS_TOKEN' in os.environ else 'Not set'}")

TRAKT_CLIENT_ID = os.environ['TRAKT_CLIENT_ID']
TRAKT_CLIENT_SECRET = os.environ['TRAKT_CLIENT_SECRET']
TRAKT_REFRESH_TOKEN = os.environ['TRAKT_REFRESH_TOKEN']
TMDB_ACCESS_TOKEN = os.environ['TMDB_ACCESS_TOKEN']

def refresh_access_token():
    print("Attempting to refresh access token...")
    response = requests.post(
        'https://api.trakt.tv/oauth/token',
        json={
            'refresh_token': TRAKT_REFRESH_TOKEN,
            'client_id': TRAKT_CLIENT_ID,
            'client_secret': TRAKT_CLIENT_SECRET,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
            'grant_type': 'refresh_token'
        }
    )
    print(f"Token refresh status code: {response.status_code}")
    print(f"Token refresh response: {response.text}")
    
    if response.status_code != 200:
        print(f"Error refreshing token. Status code: {response.status_code}")
        print(f"Response content: {response.text}")
        raise Exception("Failed to refresh token")
    
    data = response.json()
    if 'access_token' not in data:
        print(f"Unexpected response format. Received data: {data}")
        raise Exception("Access token not found in response")
    
    return data['access_token']

# Get a fresh access token
try:
    ACCESS_TOKEN = refresh_access_token()
    print("Successfully refreshed access token.")
except Exception as e:
    print(f"Failed to refresh access token: {str(e)}")
    sys.exit(1)

print("Checking environment variables:")
print(f"TRAKT_CLIENT_ID: {'Set' if 'TRAKT_CLIENT_ID' in os.environ else 'Not set'}")
print(f"TRAKT_CLIENT_SECRET: {'Set' if 'TRAKT_CLIENT_SECRET' in os.environ else 'Not set'}")
print(f"TRAKT_REFRESH_TOKEN: {'Set' if 'TRAKT_REFRESH_TOKEN' in os.environ else 'Not set'}")
print(f"TMDB_ACCESS_TOKEN: {'Set' if 'TMDB_ACCESS_TOKEN' in os.environ else 'Not set'}")

# API endpoints
TRAKT_TV_ENDPOINT = 'https://api.trakt.tv/users/me/history/shows'
TRAKT_MOVIE_ENDPOINT = 'https://api.trakt.tv/users/me/history/movies'
TMDB_TV_URL = 'https://api.themoviedb.org/3/tv/'
TMDB_MOVIE_URL = 'https://api.themoviedb.org/3/movie/'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w200'

# Headers
trakt_headers = {
    'Content-Type': 'application/json',
    'trakt-api-version': '2',
    'trakt-api-key': TRAKT_CLIENT_ID,
    'Authorization': f'Bearer {ACCESS_TOKEN}'
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

# Generate HTML
html_content = """
<div class="trakt-embed">
    <h3>Last Watched on Trakt</h3>
"""

if last_show:
    show = last_show['show']
    episode = last_show['episode']
    watched_at = datetime.fromisoformat(last_show['watched_at'].replace('Z', '+00:00'))
    image_url = get_tmdb_image(show['ids']['tmdb'], 'tv')
    html_content += f"""
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
    html_content += f"""
    <div class="item">
        <img class="item-image" src="{image_url or '/path/to/default/image.jpg'}" alt="{movie['title']}">
        <div class="item-details">
            <p><strong>Movie:</strong> {movie['title']} ({movie['year']})</p>
            <p class="timestamp">Watched: {watched_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        </div>
    </div>
    """

html_content += "</div>"

# Save HTML to file
with open('_includes/trakt_embed.html', 'w') as f:
    f.write(html_content)

print("HTML embed file generated and saved as '_includes/trakt_embed.html'")

sys.stderr.close()

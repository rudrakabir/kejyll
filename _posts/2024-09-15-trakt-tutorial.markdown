---
layout: post
title:  "Integrating Trakt.tv Watch History into a Jekyll Site"
date:   2024-09-15 08:26:03 +0530
categories: tutorial
---
#howto

This tutorial will guide you through the process of setting up an automated system to display your latest Trakt.tv watch history on your Jekyll-based website using GitHub Actions.

## Prerequisites

- A GitHub account
- A Jekyll website hosted on GitHub
- A Trakt.tv account and API access

## Step 1: Set Up Trakt.tv API Access

1. Go to [Trakt API Settings](https://trakt.tv/oauth/applications) and create a new API application.
2. Set the Redirect URI to `urn:ietf:wg:oauth:2.0:oob`.
3. Note down your Client ID and Client Secret.

## Step 2: Obtain Initial Access and Refresh Tokens

Create a file named `get_trakt_token.py` on your local machine:

```python
import requests
import webbrowser

CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Step 1: Get the authorization URL
auth_url = f"https://trakt.tv/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"

print(f"Please visit this URL to authorize the application: {auth_url}")
webbrowser.open(auth_url)

# Step 2: Get the code from user input
code = input("Enter the code from the redirect URL: ")

# Step 3: Exchange the code for an access token
token_url = "https://api.trakt.tv/oauth/token"
data = {
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code"
}

response = requests.post(token_url, json=data)
tokens = response.json()

print("Access Token:", tokens['access_token'])
print("Refresh Token:", tokens['refresh_token'])
print("Please save these tokens securely.")
```

Run this script and follow the prompts to get your initial access and refresh tokens.

## Step 3: Set Up GitHub Secrets

In your GitHub repository:
1. Go to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `TRAKT_CLIENT_ID`
   - `TRAKT_CLIENT_SECRET`
   - `TRAKT_REFRESH_TOKEN`
   - `TMDB_ACCESS_TOKEN` (if you're using TMDb for images)

## Step 4: Create the Fetch Script

Create a file named `fetch_last_watched.py` in a `scripts/` directory in your repository:

```python
import requests
import os
import sys
from datetime import datetime

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

# Close the error log file
sys.stderr.close()
```

## Step 5: Set Up GitHub Action

Create a file named `.github/workflows/update_trakt.yml` in your repository:

```yaml
name: Update Trakt Data

on:
  schedule:
    - cron: '0 */6 * * *'  # Runs every 6 hours
  workflow_dispatch:  # Allows manual triggering

jobs:
  update-trakt:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests python-dotenv
    
    - name: Run Trakt script
      env:
        TRAKT_CLIENT_ID: ${{ secrets.TRAKT_CLIENT_ID }}
        TRAKT_CLIENT_SECRET: ${{ secrets.TRAKT_CLIENT_SECRET }}
        TRAKT_REFRESH_TOKEN: ${{ secrets.TRAKT_REFRESH_TOKEN }}
        TMDB_ACCESS_TOKEN: ${{ secrets.TMDB_ACCESS_TOKEN }}
      run: |
        python scripts/fetch_last_watched.py
      continue-on-error: true
    
    - name: Check for errors
      if: failure()
      run: |
        if [ -f error_log.txt ]; then
          echo "Error log contents:"
          cat error_log.txt
        else
          echo "No error log found."
        fi
    
    - name: Commit and push if changed
      run: |
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git config --global user.name "github-actions[bot]"
        git add -A
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update Trakt data" && git push)
```

## Step 6: Include the Embed in Your Jekyll Site

In your desired Jekyll layout or page, add this line where you want the Trakt embed to appear:

```liquid
{% include trakt_embed.html %}
```

## Step 7: Add CSS Styling

Add the following CSS to your site's stylesheet (e.g., `assets/css/style.css`):

```css
.trakt-embed {
    font-family: Arial, sans-serif;
    max-width: 500px;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 8px;
    background-color: #f9f9f9;
}
.trakt-embed h3 {
    margin-top: 0;
    color: #2c3e50;
}
.trakt-embed .item {
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
    display: flex;
    align-items: start;
}
.trakt-embed .item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}
.trakt-embed .item-image {
    width: 100px;
    margin-right: 15px;
}
.trakt-embed .item-details {
    flex-grow: 1;
}
.trakt-embed p {
    margin: 5px 0;
    color: #34495e;
}
.trakt-embed .timestamp {
    font-size: 0.8em;
    color: #7f8ccd;
}
```

## Step 8: Commit and Push

Commit all these files to your repository and push them to GitHub.

## Step 9: Run the GitHub Action

1. Go to the "Actions" tab in your GitHub repository.
2. Find the "Update Trakt Data" workflow.
3. Click "Run workflow" and select your main branch.

## Maintenance

- The GitHub Action will run automatically every 6 hours to update your Trakt data.
- You can manually trigger the action anytime for immediate updates.
- If you encounter authentication errors in the future, you may need to obtain a new refresh token using the `get_trakt_token.py` script and update the `TRAKT_REFRESH_TOKEN` secret in your GitHub repository.

That's it! Your Jekyll site should now display your latest Trakt.tv watch history, automatically updating every 6 hours.

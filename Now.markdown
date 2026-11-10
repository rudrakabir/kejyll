---
layout: page
title: Now
permalink: /Now/
---
Updated 11th Oct, 2024 on a rainy morning in Ahmedabad.

# Dance and Garba
This year was the first time I actively and enthusiastically participated in Navratri dancing and Garba, and I really really enjoyed it. I didn't know my body could move like that. 

# Building an online identity
I am gradually getting more comfortable with putting myself out there on the Wild Wild Web, and letting myself be perceived to further my plans for world domination. So far, it is not so bad. 

# Website
I've been noodling about on this website as a live server on my local machine for a few months now, for no particular reason. I think I spent a couple weeks just making the same posts in different static site generators just to check it out. It's not done yet, but it's a great start and I love it. [Just get it down](https://darn.es/just-get-it-done/), something I read just today, captures this well. 


# Body
I have been heavily focused on taking care of my body. I started going to the gym regularly, worked on fixing my diet and sleep schedules, and the payoff has been marvelous. I also went to Himachal for a month in June for a Yoga course, to further that same quest. I am absolutely loving that, and I have reaped so much from it. 

# Music
[last.fm](https://www.last.fm/user/rudrakabir) is basically a direct conduit into what the inside of my head feels like which is kinda wack if you ask me.

I am really enjoying Sabrina Carpenter right now, as well as the movie album from Lakshya.

<div class="lastfm-embed" id="now-lastfm-widget">
  <h3>Recently Played on Last.fm</h3>
  <ol class="lastfm-items" aria-label="Recent completed scrobbles"></ol>
  <p class="lastfm-status" role="status"></p>
  <p><a href="https://www.last.fm/user/rudrakabir">View my listening history on Last.fm</a></p>
</div>
<style>
  #now-lastfm-widget { max-width: 500px; padding: 15px; margin: 15px 0; border: 1px solid #ddd; border-radius: 8px; background: #f9f9f9; font-family: Arial, sans-serif; color: #34495e; }
  #now-lastfm-widget h3 { margin-top: 0; color: #2c3e50; }
  #now-lastfm-widget .lastfm-items { list-style: none; padding: 0; margin: 0; }
  #now-lastfm-widget li { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #eee; }
  #now-lastfm-widget li:last-child { border-bottom: 0; }
  #now-lastfm-widget img { width: 48px; height: 48px; flex: 0 0 48px; object-fit: cover; border-radius: 3px; }
  #now-lastfm-widget .lastfm-details { min-width: 0; overflow-wrap: anywhere; }
  #now-lastfm-widget .lastfm-title { font-weight: bold; }
  #now-lastfm-widget .lastfm-meta { font-size: .85em; }
  #now-lastfm-widget p { margin: 5px 0; }
  #now-lastfm-widget .lastfm-status:empty { display: none; }
</style>
<script>
(() => {
  const widget = document.getElementById('now-lastfm-widget');
  const target = widget.querySelector('.lastfm-items');
  const status = widget.querySelector('.lastfm-status');
  const feed = 'https://raw.githubusercontent.com/rudrakabir/LastFM-Embed/codex/lastfm-feed/lastfm_data.json';
  function safeURL(value, hosts) {
    if (typeof value !== 'string') return null;
    try {
      const url = new URL(value);
      return url.protocol === 'https:' && hosts.includes(url.hostname) &&
        !url.username && !url.password && !url.port && !url.search && !url.hash ? url : null;
    } catch (_) { return null; }
  }
  function card(item) {
    if (!item || typeof item.title !== 'string' || !item.title.trim() ||
        typeof item.artist !== 'string' || !item.artist.trim() ||
        typeof item.album !== 'string' || !Number.isSafeInteger(item.played_at) || item.played_at <= 0) {
      throw new Error('Invalid scrobble');
    }
    const link = safeURL(item.url, ['www.last.fm', 'last.fm']);
    if (!link || !link.pathname.startsWith('/music/')) throw new Error('Invalid track link');
    const row = document.createElement('li');
    const art = safeURL(item.image, ['lastfm.freetls.fastly.net']);
    if (art && !art.pathname.includes('2a96cbd8b46e442fc41c2b86b821562f')) {
      const image = document.createElement('img');
      image.alt = '';
      image.width = image.height = 48;
      image.loading = 'lazy';
      image.referrerPolicy = 'no-referrer';
      image.addEventListener('error', () => image.remove(), { once: true });
      image.src = art.href;
      row.append(image);
    }
    const details = document.createElement('div');
    details.className = 'lastfm-details';
    const title = document.createElement('a');
    title.className = 'lastfm-title';
    title.href = link.href;
    title.textContent = item.title;
    const meta = document.createElement('div');
    meta.className = 'lastfm-meta';
    meta.textContent = item.artist + (item.album ? ' · ' + item.album : '');
    details.append(title, meta);
    row.append(details);
    return row;
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  fetch(feed, { credentials: 'omit', signal: controller.signal })
    .then(response => {
      if (!response.ok) throw new Error('Feed unavailable');
      return response.json();
    })
    .then(data => {
      if (data.version !== 1 || data.user !== 'rudrakabir' || !Array.isArray(data.items) || data.items.length !== 5) {
        throw new Error('Invalid feed');
      }
      const rows = data.items.map(card);
      target.replaceChildren(...rows);
    })
    .catch(() => { status.textContent = 'Recent tracks are temporarily unavailable.'; })
    .finally(() => clearTimeout(timeout));
})();
</script>


# Reading
I am working my way through Human Universals, by Donald Brown. I came across it from the wikipedia article on Human Universals, which I thought was really interesting. Basically, there are certain things that cultures develop independently, called universals. 



## X-risk
I am really obsessing over the current issues around the existential risks that are facing humanity right now. We have never been more able to wipe ourselves off the face off the planet, and that this can now be done _on accident_ scares me. 

Includes but not limited to climate change, AI S-risk, and of course the usual suspects of war famine and pestilence.




<div class="trakt-embed" id="now-trakt-widget">
  <h3>Last Watched on Trakt</h3>
  <div class="trakt-items"></div>
  <p><a href="https://trakt.tv/users/rudrakabir/history">View my watch history on Trakt</a></p>
</div>
<script>
(() => {
  const target = document.querySelector('#now-trakt-widget .trakt-items');
  const feed = 'https://raw.githubusercontent.com/rudrakabir/Trakt-Embed/main/trakt_data.json';
  const dateFormat = new Intl.DateTimeFormat(undefined, {
    day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'
  });
  function detail(parent, label, value) {
    const row = document.createElement('p');
    const name = document.createElement('strong');
    name.textContent = label + ':';
    row.append(name, ' ' + value);
    parent.append(row);
  }
  function card(item) {
    if (!item || typeof item.title !== 'string' || !item.title.trim() ||
        item.date_precision !== 'day' || !/^\d{4}-\d{2}-\d{2}$/.test(item.watched_at)) {
      throw new Error('Invalid Trakt feed entry');
    }
    const watched = new Date(item.watched_at);
    if (Number.isNaN(watched.valueOf()) || watched.toISOString().slice(0, 10) !== item.watched_at) {
      throw new Error('Invalid Trakt watch date');
    }
    const row = document.createElement('div');
    row.className = 'item';
    if (typeof item.poster === 'string' && /^https:\/\/image\.tmdb\.org\/t\/p\/w200\/[A-Za-z0-9_.-]+$/.test(item.poster)) {
      const image = document.createElement('img');
      image.className = 'item-image';
      image.alt = '';
      image.loading = 'lazy';
      image.src = item.poster;
      row.append(image);
    }
    const details = document.createElement('div');
    details.className = 'item-details';
    detail(details, item.type === 'episodes' ? 'TV Show' : 'Movie', item.title);
    if (item.type === 'episodes' && typeof item.episode === 'string') {
      detail(details, 'Episode', item.episode);
    }
    const timestamp = document.createElement('p');
    timestamp.className = 'timestamp';
    const time = document.createElement('time');
    time.dateTime = item.watched_at;
    time.textContent = dateFormat.format(watched);
    timestamp.append('Watched: ', time);
    details.append(timestamp);
    row.append(details);
    return row;
  }
  fetch(feed, { credentials: 'omit' })
    .then(response => {
      if (!response.ok) throw new Error('Trakt feed unavailable');
      return response.json();
    })
    .then(data => {
      if (data.version !== 1 || !Array.isArray(data.items)) throw new Error('Invalid Trakt feed');
      const cards = ['episodes', 'movies'].map(type => card(data.items.find(item => item?.type === type)));
      target.replaceChildren(...cards);
    })
    .catch(() => { target.textContent = 'Recent watch history is temporarily unavailable.'; });
})();
</script>

Inspired by [sive.rs](https://sive.rs/now) but with my own spin on it.

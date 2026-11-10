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

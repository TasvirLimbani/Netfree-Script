# # import os
# # import requests

# # # ==================== CONFIGURATION ====================
# # BOT_TOKEN = "8107792855:AAG6c_hef5qR1YBxgiVk6lN6poHtxXLXa9U"  # Get this from @BotFather
# # CHANNEL_ID = "-1003372872571"  # Your Telegram channel username or ID
# import os
# import requests

# # ==================== CONFIGURATION ====================
# BOT_TOKEN = "8107792855:AAG6c_hef5qR1YBxgiVk6lN6poHtxXLXa9U"  # Get this from @BotFather
# CHANNEL_ID = "-1003372872571"  # Your Telegram channel username or ID

# # TMDB API Endpoint provided
# TMDB_API_URL = "https://api.themoviedb.org/3/trending/movie/day?api_key=ce20e7cf6328f6174905bf11f6e0ea5d&page=1"
# TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
# TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# # File to store IDs of already posted items (duplicate prevention)
# POSTED_LOG_FILE = "posted_movies.txt"

# # TMDB Genre ID mapping dictionary
# GENRE_MAP = {
#     28: "Action",
#     12: "Adventure",
#     16: "Animation",
#     35: "Comedy",
#     80: "Crime",
#     99: "Documentary",
#     18: "Drama",
#     10751: "Family",
#     14: "Fantasy",
#     36: "History",
#     27: "Horror",
#     10402: "Music",
#     9648: "Mystery",
#     10749: "Romance",
#     878: "SciFi",
#     10770: "TVMovie",
#     53: "Thriller",
#     10752: "War",
#     38: "Western",
# }
# # =======================================================


# def load_posted_ids():
#   """Loads already posted item IDs from the local text file."""
#   if not os.path.exists(POSTED_LOG_FILE):
#     return set()
#   with open(POSTED_LOG_FILE, "r") as f:
#     return set(line.strip() for line in f if line.strip())


# def save_posted_id(movie_id):
#   """Saves a newly posted item ID to the text file."""
#   with open(POSTED_LOG_FILE, "a") as f:
#     f.write(f"{movie_id}\n")


# def get_media_title(item):
#   """Safely extracts title or name regardless of what TMDB returns."""
#   return (
#       item.get("title")
#       or item.get("name")
#       or item.get("original_title")
#       or item.get("original_name")
#       or "Unknown Title"
#   )


# def get_genre_hashtags(genre_ids):
#   """Converts TMDB numeric genre IDs into SEO-friendly hashtags."""
#   names = [GENRE_MAP.get(gid, "Entertainment") for gid in genre_ids]
#   return (
#       " ".join([f"#{name}" for name in names]) if names else "#Drama #Movie"
#   )


# def format_movie_caption(movie):
#   """Formats media details with tap-to-copy title style and safe HTML."""
#   genres_tags = get_genre_hashtags(movie.get("genre_ids", []))
#   release_date = (
#       movie.get("release_date")
#       or movie.get("first_air_date")
#       or "2026-09-16"
#   )

#   title = get_media_title(movie)
#   overview = movie.get("overview", "No overview available.")
#   language = movie.get("original_language", "en").upper()
#   rating = round(movie.get("vote_average", 0.0), 1)

#   star_count = round(rating / 2)
#   stars = "⭐" * max(1, min(star_count, 5))
#   title_keyword = title.replace(" ", "").replace(":", "").replace("-", "")

#   caption = (
#       f"🎬 <b>NETFREE | <code>{title}</code></b> 🚀\n\n"
#       f"<b><code>{title}</code></b> is a trending feature release streaming now on Netfree.\n\n"
#       f"📖 <b>Synopsis & Overview:</b>\n"
#       f"<i>{overview}</i>\n\n"
#       f"🎭 <b>Genre:</b> {genres_tags}\n"
#       f"🗣️ <b>Language:</b> {language}\n"
#       f"📅 <b>Release Date:</b> {release_date}\n"
#       f"{stars} <b>IMDb/TMDB Rating:</b> <b>{rating}/10</b>\n\n"
#       f'🌐 <b>Official Website:</b> <a href="https://netfree.co.in">netfree.co.in</a>\n\n'
#       f'📱 <b>Download Android App:</b> <a href="https://play.google.com/store/apps/details?id=com.netfree.mobile.app&referrer=utm_source%3Dradhe%26utm_campaign%3Dradhe%26anid%3Dadmob">DOWNLOAD APP</a>\n\n'
#       f"👉 <b>Join @netfree_coral for Free Streaming & Daily Updates!</b>\n\n"
#       f"#Netfree #FreeStreaming #LatestMovies #HDMovies #WebSeries "
#       f"#{title_keyword} #WatchOnline #BlockbusterMovies #CinemaHub"
#   )
#   return caption


# def fetch_and_post_movies():
#   """Fetches trending items and posts the next unposted title/name securely."""
#   print("🔄 Fetching trending data from TMDB...")
#   try:
#     response = requests.get(TMDB_API_URL)
#     data = response.json()
#     movies = data.get("results", [])

#     if not movies:
#       print("⚠️ No items found from TMDB API.")
#       return

#     posted_ids = load_posted_ids()
#     new_movie_found = False

#     for movie in movies:
#       movie_id = str(movie.get("id"))
#       title = get_media_title(movie)

#       # Skip if already posted
#       if movie_id in posted_ids:
#         print(f"⏩ Skipping '{title}' (Already posted)")
#         continue

#       poster_path = movie.get("poster_path")
#       if not poster_path:
#         print(f"⚠️ Skipping '{title}' (No poster image available)")
#         continue

#       # We found the next unposted item!
#       poster_url = f"{TMDB_IMAGE_BASE}{poster_path}"
#       caption_text = format_movie_caption(movie)

#       payload = {
#           "chat_id": CHANNEL_ID,
#           "photo": poster_url,
#           "caption": caption_text,
#           "parse_mode": "HTML",
#       }

#       print(f"🚀 Sending SEO-optimized post for '{title}' to Telegram...")
#       res = requests.post(TELEGRAM_API_URL, data=payload)
#       res_json = res.json()

#       if res_json.get("ok"):
#         print(f"✅ Successfully posted: {title}")
#         save_posted_id(movie_id)
#         new_movie_found = True
#         break
#       else:
#         print(f"❌ Failed to post {title}: {res_json.get('description')}")
#         break

#     if not new_movie_found:
#       print(
#           "✨ No new unposted content found on this page! All are up to date."
#       )

#   except Exception as e:
#     print(f"❌ Error during execution: {e}")


# # ==================== EXECUTION ====================
# if __name__ == "__main__":
#   if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
#     print("⚠️ Please replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token.")
#   else:
#     fetch_and_post_movies()

import os
import sys
import time
import requests

# ==================== CONFIGURATION ====================
BOT_TOKEN = "8107792855:AAG6c_hef5qR1YBxgiVk6lN6poHtxXLXa9U"  # Your Telegram Bot Token
CHANNEL_ID = "-1003372872571"  # Your Telegram Channel ID

# TMDB API Endpoint provided
TMDB_API_URL = "https://api.themoviedb.org/3/trending/tv/day?api_key=ce20e7cf6328f6174905bf11f6e0ea5d&page=1"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# File to store IDs of already posted items (duplicate prevention)
POSTED_LOG_FILE = "posted_movies.txt"

# TMDB Genre ID mapping dictionary
GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "SciFi",
    10770: "TVMovie",
    53: "Thriller",
    10752: "War",
    38: "Western",
}
# =======================================================


def load_posted_ids():
  """Loads already posted item IDs from the local text file."""
  if not os.path.exists(POSTED_LOG_FILE):
    return set()
  with open(POSTED_LOG_FILE, "r") as f:
    return set(line.strip() for line in f if line.strip())


def save_posted_id(movie_id):
  """Saves a newly posted item ID to the text file."""
  with open(POSTED_LOG_FILE, "a") as f:
    f.write(f"{movie_id}\n")


def get_media_title(item):
  """Safely extracts title or name regardless of what TMDB returns."""
  return (
      item.get("title")
      or item.get("name")
      or item.get("original_title")
      or item.get("original_name")
      or "Unknown Title"
  )


def get_genre_hashtags(genre_ids):
  """Converts TMDB numeric genre IDs into SEO-friendly hashtags."""
  names = [GENRE_MAP.get(gid, "Entertainment") for gid in genre_ids]
  return (
      " ".join([f"#{name}" for name in names]) if names else "#Drama #Movie"
  )


def format_movie_caption(movie):
  """Formats media details with tap-to-copy title style and safe HTML."""
  genres_tags = get_genre_hashtags(movie.get("genre_ids", []))
  release_date = (
      movie.get("release_date")
      or movie.get("first_air_date")
      or "2026-09-16"
  )

  title = get_media_title(movie)
  overview = movie.get("overview", "No overview available.")
  language = movie.get("original_language", "en").upper()
  rating = round(movie.get("vote_average", 0.0), 1)

  star_count = round(rating / 2)
  stars = "⭐" * max(1, min(star_count, 5))
  title_keyword = title.replace(" ", "").replace(":", "").replace("-", "")

  caption = (
      f"🎬 <b>NETFREE | <code>{title}</code></b> 🚀\n\n"
      f"<b><code>{title}</code></b> is a trending feature release streaming now on Netfree.\n\n"
      f"📖 <b>Synopsis & Overview:</b>\n"
      f"<i>{overview}</i>\n\n"
      f"🎭 <b>Genre:</b> {genres_tags}\n"
      f"🗣️ <b>Language:</b> {language}\n"
      f"📅 <b>Release Date:</b> {release_date}\n"
      f"{stars} <b>IMDb/TMDB Rating:</b> <b>{rating}/10</b>\n\n"
      f'🌐 <b>Official Website:</b> <a href="https://netfree.co.in">netfree.co.in</a>\n\n'
      f'📱 <b>Download Android App:</b> <a href="https://play.google.com/store/apps/details?id=com.netfree.mobile.app&referrer=utm_source%3Dradhe%26utm_campaign%3Dradhe%26anid%3Dadmob">DOWNLOAD APP</a>\n\n'
      f"👉 <b>Join @netfree for Free Streaming & Daily Updates!</b>\n\n"
      f"#Netfree #FreeStreaming #LatestMovies #HDMovies #WebSeries "
      f"#{title_keyword} #WatchOnline #BlockbusterMovies #CinemaHub"
  )
  return caption


def fetch_and_post_movies():
  """Fetches trending items and posts the next unposted title/name securely."""
  print("🔄 Fetching trending data from TMDB...")
  sys.stdout.flush()
  try:
    response = requests.get(TMDB_API_URL, timeout=15)
    data = response.json()
    movies = data.get("results", [])

    if not movies:
      print("⚠️ No items found from TMDB API.")
      sys.stdout.flush()
      return

    posted_ids = load_posted_ids()
    new_movie_found = False

    for movie in movies:
      movie_id = str(movie.get("id"))
      title = get_media_title(movie)

      # Skip if already posted
      if movie_id in posted_ids:
        print(f"⏩ Skipping '{title}' (Already posted)")
        sys.stdout.flush()
        continue

      poster_path = movie.get("poster_path")
      if not poster_path:
        print(f"⚠️ Skipping '{title}' (No poster image available)")
        sys.stdout.flush()
        continue

      # We found the next unposted item!
      poster_url = f"{TMDB_IMAGE_BASE}{poster_path}"
      caption_text = format_movie_caption(movie)

      payload = {
          "chat_id": CHANNEL_ID,
          "photo": poster_url,
          "caption": caption_text,
          "parse_mode": "HTML",
      }

      print(f"🚀 Sending SEO-optimized post for '{title}' to Telegram...")
      sys.stdout.flush()
      res = requests.post(TELEGRAM_API_URL, data=payload, timeout=15)
      res_json = res.json()

      if res_json.get("ok"):
        print(f"✅ Successfully posted: {title}")
        save_posted_id(movie_id)
        new_movie_found = True
        sys.stdout.flush()
        break
      else:
        print(f"❌ Failed to post {title}: {res_json.get('description')}")
        sys.stdout.flush()
        break

    if not new_movie_found:
      print("✨ No new unposted content found on this page! All are up to date.")
      sys.stdout.flush()

  except Exception as e:
    print(f"❌ Error during execution: {e}")
    sys.stdout.flush()


# ==================== EXECUTION (24/7 LIFETIME LOOP) ====================
if __name__ == "__main__":
  print(
      "🤖 Netfree Remote Desktop Auto-Poster Initialized! Running every 1"
      " hour..."
  )
  sys.stdout.flush()

  while True:
    fetch_and_post_movies()
    print("⏳ Waiting 1 hour for the next automatic run...\n")
    sys.stdout.flush()
    time.sleep(3600)  # Sleep for 3600 seconds (1 hour)

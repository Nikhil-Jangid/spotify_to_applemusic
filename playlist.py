import os
import subprocess
import difflib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials from .env file
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Function to initialize Spotify API
def initialize_spotify():
    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                               client_secret=SPOTIFY_CLIENT_SECRET))

# Function to find the path of the song in local storage
def find_song_path(artist_name, album_name, song_name):
    try:
        local_files = os.listdir(f"/Users/nikhiljangid/Music/Music/Media/Music/{artist_name}/{album_name}")
        similar_names = difflib.get_close_matches(song_name, local_files)
        if similar_names:
            song_path = f"/Users/nikhiljangid/Music/Music/Media/Music/{artist_name}/{album_name}/{similar_names[0]}"
            logging.info(f"Song Path: {song_path}")
            return song_path
        else:
            logging.warning(f"Song Path not found for: {song_name}")
            return None
    except FileNotFoundError:
        logging.warning(f"Song Path not found for: {song_name}")
        return None

# Function to add song to Apple Music playlist
def add_song_to_apple_music_playlist(playlist_name, song_path):
    escaped_path = song_path.replace('"', '\\"')  # Escape double quotes
    script = f"""
    tell application "Music"
        set newPlaylist to user playlist "{playlist_name}"
        add POSIX file "{escaped_path}" to newPlaylist
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error adding song {song_path}: {result.stderr}")
        return False
    else:
        logging.info(f"Added song {song_path} to playlist {playlist_name}")
        return True

# Function to get songs from Spotify playlist
def get_spotify_playlist_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    spotify_songs = []
    for item in results['items']:
        track = item['track']
        song_name = track['name']
        artist_name = track['artists'][0]['name'] if track['artists'] else None
        album_name = track['album']['name'] if track['album'] else None
        spotify_songs.append((song_name, artist_name, album_name))
    return spotify_songs

# Function to get songs from Apple Music playlist
def get_apple_music_playlist_tracks(playlist_name):
    script = f"""
    tell application "Music"
        set track_names to name of tracks of user playlist "{playlist_name}"
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    apple_music_songs = result.stdout.strip().split(", ")
    return apple_music_songs

# Function to merge songs from Spotify and Apple Music playlists
def merge_songs(sp, spotify_songs, apple_music_songs, playlist_name):
    not_found_tracks = []
    for song in spotify_songs:
        song_name = song[0]
        if song_name not in apple_music_songs:
            logging.warning(f"Song not found in Apple Music: {song_name}")
            not_found_tracks.append(song)
    return not_found_tracks

# Main function
def main():
    # Initialize Spotify API
    sp = initialize_spotify()

    # Spotify Playlist ID
    spotify_playlist_id = input("Enter the Spotify Playlist ID: ")

    # Apple Music Playlist Name
    apple_music_playlist_name = input("Enter the Apple Music Playlist Name: ")

    # Get songs from Spotify playlist
    spotify_songs = get_spotify_playlist_tracks(sp, spotify_playlist_id)

    # Get songs from Apple Music playlist
    apple_music_songs = get_apple_music_playlist_tracks(apple_music_playlist_name)

    # Merge songs from both playlists
    not_found_tracks = merge_songs(sp, spotify_songs, apple_music_songs, apple_music_playlist_name)

    # Add matched songs to Apple Music playlist
    songs_added = 0
    songs_skipped = []
    for song in not_found_tracks:
        song_name, artist_name, album_name = song
        song_path = find_song_path(artist_name, album_name, song_name)
        if song_path:
            songs_added += add_song_to_apple_music_playlist(apple_music_playlist_name, song_path)
        else:
            songs_skipped.append(f"{song_name} | Artist: {artist_name} | Album: {album_name}")

    logging.info(f"Total songs added: {songs_added}")
    logging.info("Songs skipped due to missing location:")
    for song in songs_skipped:
        logging.warning(song)

if __name__ == "__main__":
    main()

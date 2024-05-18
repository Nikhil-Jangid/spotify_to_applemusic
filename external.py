import os
import shutil
import subprocess
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create an Apple Music playlist using AppleScript
def create_apple_music_playlist(playlist_name):
    escaped_name = re.sub(r'[^\w\s]', '', playlist_name)  # Remove special characters
    script = f"""
    tell application "Music"
        if not (exists (user playlist "{escaped_name}")) then
            set newPlaylist to make new user playlist with properties {{name:"{escaped_name}"}}
        end if
    end tell
    """
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error(f"Error creating playlist {playlist_name}: {result.stderr}")
    else:
        logging.info(f"Created or verified playlist {playlist_name}")

# Function to add songs to the Apple Music playlist using AppleScript
def add_songs_to_apple_music_playlist(playlist_name, song_paths):
    for song_path in song_paths:
        escaped_path = song_path.replace('"', '\\"')  # Escape double quotes
        script = f"""
        tell application "Music"
            set newPlaylist to user playlist "{playlist_name}"
            add POSIX file "{escaped_path}" to newPlaylist
        end tell
        """
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Error adding song {song_path} to playlist {playlist_name}: {result.stderr}")
        else:
            logging.info(f"Added song {song_path} to playlist {playlist_name}")

# Function to merge songs from all folders
def merge_songs_from_folders(folder_paths):
    merged_songs = []
    for folder_path in folder_paths:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".mp3", ".m4a", ".wav")):  # Add more file extensions if needed
                    song_path = os.path.join(root, file)
                    if song_path not in merged_songs:
                        merged_songs.append(song_path)
    return merged_songs

# Function to copy music files from external drive to local directory
def copy_music_files(source_dir, destination_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith((".mp3", ".m4a", ".wav")):  # Add more file extensions if needed
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                if not os.path.exists(destination_path):
                    shutil.copy2(source_path, destination_path)
                    logging.info(f"Copied {source_path} to {destination_path}")
                else:
                    logging.info(f"File {destination_path} already exists, skipping copy.")

# Main function
def main():
    external_drive = "/Volumes/EXTERNAL"  # Replace with the path to your external drive
    local_music_dir = "/Users/USERNAME/Music/Media"  # Replace with the path to your local music directory
    playlists = ["Playlist1", "Playlist2", "Playlist3"]  # Add your playlist names here

    folder_paths = [os.path.join(external_drive, playlist_name) for playlist_name in playlists]
    
    # Merge songs from all folders
    merged_songs = merge_songs_from_folders(folder_paths)
    
    # Copy music files
    for folder_path in folder_paths:
        copy_music_files(folder_path, local_music_dir)
    
    # Create playlists in Apple Music
    for playlist_name in playlists:
        create_apple_music_playlist(playlist_name)
    
    # Add merged songs to respective playlists
    for playlist_name in playlists:
        add_songs_to_apple_music_playlist(playlist_name, merged_songs)

if __name__ == "__main__":
    main()

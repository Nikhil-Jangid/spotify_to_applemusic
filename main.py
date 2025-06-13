import os
import subprocess

# Function to import MP3 files to Apple Music and get their track references
def import_songs_from_folder(folder_path):
    track_references = []
    for mp3_file in os.listdir(folder_path):
        if mp3_file.endswith('.mp3'):
            mp3_path = os.path.join(folder_path, mp3_file)
            script = f'''
            tell application "Music"
                set theTrack to (add POSIX file "{mp3_path}")
                return id of theTrack
            end tell
            '''
            process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                print(f"Error importing {mp3_file}: {stderr.decode('utf-8')}")
            else:
                track_id = stdout.decode('utf-8').strip()
                track_references.append(track_id)
                print(f"Imported {mp3_file} to Apple Music with track ID {track_id}.")
    return track_references

# Function to create a playlist and add songs to it
def create_playlist_and_add_songs(playlist_name, track_references):
    # Create the playlist
    script = f'''
    tell application "Music"
        activate
        set newPlaylist to make new user playlist with properties {{name:"{playlist_name}"}}
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"Error creating playlist: {stderr.decode('utf-8')}")
        return

    # Add each track to the playlist using its reference
    for track_id in track_references:
        script = f'''
        tell application "Music"
            set newPlaylist to user playlist "{playlist_name}"
            set theTrack to some track whose id is {track_id}
            duplicate theTrack to newPlaylist
        end tell
        '''
        process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Error adding track with ID {track_id} to playlist: {stderr.decode('utf-8')}")
        else:
            print(f"Added track with ID {track_id} to playlist '{playlist_name}'.")

# Main script
# Set the root folder where all playlist folders are stored
root_folder = input("Enter the path to the root folder containing your playlist folders: ")

# Get the list of playlist folders
playlist_folders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]

# Import all songs from each folder into Apple Music and collect their track references
playlist_tracks = {}
for playlist_folder in playlist_folders:
    folder_path = os.path.join(root_folder, playlist_folder)
    track_references = import_songs_from_folder(folder_path)
    playlist_tracks[playlist_folder] = track_references

# Create playlists and add songs to them
for playlist_folder in playlist_folders:
    track_references = playlist_tracks[playlist_folder]
    create_playlist_and_add_songs(playlist_folder, track_references)
import os
import subprocess

# Function to get the list of tracks in a specific playlist
def get_tracks_in_playlist(playlist_name):
    script = f'''
    tell application "Music"
        set trackList to {{}}
        set thePlaylist to user playlist "{playlist_name}"
        repeat with aTrack in (every track of thePlaylist)
            set end of trackList to {id:aTrack's id, name:aTrack's name, artist:aTrack's artist, album:aTrack's album}
        end repeat
        return trackList
    end tell
    '''
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        print(f"Error getting tracks in playlist '{playlist_name}': {stderr.decode('utf-8')}")
        return []
    else:
        return eval(stdout.decode('utf-8'))

# Function to import MP3 files to Apple Music and get their track references
def import_songs_from_folder(folder_path, existing_tracks):
    track_references = []
    for mp3_file in os.listdir(folder_path):
        if mp3_file.endswith('.mp3'):
            mp3_path = os.path.join(folder_path, mp3_file)
            file_name = os.path.splitext(mp3_file)[0]
            is_existing = any(track for track in existing_tracks if track['name'] == file_name)
            if not is_existing:
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
            else:
                print(f"{mp3_file} already exists in Apple Music.")
    return track_references

# Function to update the playlist with new songs
def update_playlist_with_songs(playlist_name, folder_path):
    # Get the list of existing tracks in the playlist
    existing_tracks = get_tracks_in_playlist(playlist_name)

    # Import new songs from the folder into Apple Music
    new_tracks = import_songs_from_folder(folder_path, existing_tracks)
    
    # Add new tracks to the playlist
    for track_id in new_tracks:
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
            print(f"Error adding track with ID {track_id} to playlist '{playlist_name}': {stderr.decode('utf-8')}")
        else:
            print(f"Added track with ID {track_id} to playlist '{playlist_name}'.")

# Main script
# Set the root folder where all playlist folders are stored
root_folder = input("Enter the path to the root folder containing your playlist folders: ")

# Get the list of playlist folders
playlist_folders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]

# Update each playlist with new songs from the corresponding folder
for playlist_folder in playlist_folders:
    folder_path = os.path.join(root_folder, playlist_folder)
    update_playlist_with_songs(playlist_folder, folder_path)

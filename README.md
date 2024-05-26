# Playlist Transfer Tool

This Python script facilitates the transfer of songs from a Spotify playlist to an Apple Music playlist. It leverages the Spotify and Apple Music APIs to achieve this. Additionally, it utilizes the spotdl tool to download songs from Spotify.

## Features

- Transfer songs from a Spotify playlist to an Apple Music playlist.
- Handle missing songs by logging and skipping them.
- Provide detailed logging for tracking script execution and errors.
- Input validation for Spotify playlist ID and Apple Music playlist name.
- Download songs from Spotify using [spotdl](https://github.com/spotDL/spotify-downloader).

## Prerequisites

Before using this tool, ensure you have the following:

- Spotify Developer Account: You'll need to create a Spotify Developer account and register your application to obtain the necessary credentials.
- Python 3: Make sure you have Python 3 installed on your system.
- spotdl: Install spotdl and download songs from Your Spotify Playlist. You can find installation instructions [here](https://github.com/spotDL/spotify-downloader).

## Setup

1. Clone the repository:

```
git clone https://github.com/Nikhil-Jangid/playlist-transfer-tool.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a .env file using .env.example in the project directory and add your Spotify API credentials:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

4. Update Path of ```local_files``` and ```song_path``` in playlist.py with the location where the songs are located.

5. Run the script:
```
python playlist.py
```

## About external.py and internal.py

### external.py

**Purpose:**
- `external.py` is designed to interact with external systems or resources outside the local environment.
- It contains functions for tasks such as:
  - Copying files from an external drive to a local directory.
  - Creating Apple Music playlists using AppleScript.
  - Adding songs to Apple Music playlists using AppleScript.
- This script is useful when you need to perform operations that involve external resources, like transferring files or interacting with external applications like Apple Music.

**Usage Scenarios:**
- **File Transfer:** When you need to copy files from an external drive or directory to your local machine.
- **Apple Music Playlist Management:** When you want to automate the creation and management of Apple Music playlists, especially when integrating with other systems or scripts.

**Example Applications:**
- Suppose you have a collection of music files stored on an external hard drive, and you want to organize them into specific playlists in your Apple Music library. You can use `external.py` to copy these files to your local machine and then create and populate playlists on Apple Music accordingly.

### internal.py

**Purpose:**
- `internal.py` is intended for internal operations within the local environment.
- It includes functions for tasks like:
  - Merging songs from different folders on the local machine.
  - Creating Apple Music playlists using AppleScript.
  - Adding songs to Apple Music playlists using AppleScript.
- This script is useful when you need to perform operations that involve local files or applications, without interacting with external resources.

**Usage Scenarios:**
- **Local File Management:** When you need to work with files and directories stored locally on your machine.
- **Apple Music Playlist Management:** Similar to `external.py`, for automating tasks related to Apple Music playlists, but focusing on operations within the local environment.

**Example Applications:**
- If you have multiple folders containing music files on your computer, and you want to merge them into specific playlists in your Apple Music library, you can use `internal.py` to scan the local directories, merge the songs, and then create and populate playlists on Apple Music accordingly.

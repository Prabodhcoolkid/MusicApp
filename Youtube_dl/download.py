from subprocess import run
import youtube_dl
# Code for downloading a list of links

def download_songs():
        # Specify the path to your text file
    file_path = './music.txt'

    # Read the links from the text file and create a list
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file.readlines()]

    # Print the list of links (optional)
    
    path = "./downloaded_songs"
    for link in links:
        print("downloading\n")
        run(f'youtube-dl --prefer-ffmpeg -o "{path}/%(title)s.%(ext)s" --extract-audio --audio-format mp3 {link}',
                shell=True, capture_output=True, text=True).stdout

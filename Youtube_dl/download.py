# Code for downloading a list of links

def download_songs():
    links = []
    path = ""
    for link in links:
        run(f'youtube-dl --prefer-ffmpeg -o "{path}/%(title)s.%(ext)s" --extract-audio --audio-format mp3 {link}',
                shell=True, capture_output=True, text=True).stdout
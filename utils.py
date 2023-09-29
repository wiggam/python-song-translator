import requests
import keys
import sys
from lyricsgenius import Genius
from languages import LANGUAGES
from mtranslate import translate

CLIENT_ID = keys.client_id
CLIENT_SECRET = keys.client_secret


def get_access_token():
    # Prepare data for the token request
    token_url = "https://api.genius.com/oauth/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    # Make a POST request to obtain an access token
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        # Extract the access token from the response
        return response.json().get('access_token')
    else:
        print(f'Error: {response.status_code}')
        sys.exit


def song_search(title, access_token):
    # Now, you can use the access token to make authenticated requests to the Genius API
    search_url = "https://api.genius.com/search"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': title
    }

    # Make a GET request to search for the query
    search_response = requests.get(search_url, headers=headers, params=params)

    if search_response.status_code == 200:
        search_data = search_response.json()

        # create search result dictionary
        results = []
        for key in search_data['response']['hits']:
            song_dict = {}
            song = key['result']  # Get the 'result' dictionary for each song
            song_dict['full_title'] = song['full_title']
            song_dict['id'] = song['id']
            results.append(song_dict)
        return results

    else:
        print(f'Error: {search_response.status_code}')
        sys.exit


def lyrics_search(id, song_title, access_token):
    # create genius class
    genius = Genius(access_token)
    # Turn off status messages
    genius.verbose = False

    # Remove section headers (e.g. [Chorus]) from lyrics when searching
    genius.remove_section_headers = True

    # Include hits thought to be non-songs (e.g. track lists)
    genius.skip_non_songs = False

    # Exclude songs with these words in their title
    genius.excluded_terms = ["(Remix)", "(Live)"]

    lyrics = genius.lyrics(id)
    if lyrics:
        with open(f'{song_title}.txt', 'w', encoding='utf-8') as file:
            file.write(lyrics)
        return lyrics
    else:
        print(f"No lyrics found for {song_title}")


def print_languages():
    for code, lang in LANGUAGES.items():
        print(f"{code}: {lang}")


def translate_song(text, src_lang, dest_lang):
    # read original song
    with open(f'{text}.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # write translation
    with open(f'{text}.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            line = line.strip()

            # Check if it's a non-empty line
            if line:
                # translate line
                translated_line = translate(
                    line, dest_lang, src_lang)

                file.write(f'{line}\n({translated_line})\n\n')

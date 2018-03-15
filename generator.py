#! /usr/bin/env python3
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import sys
from collections import Counter
from nltk.tokenize import word_tokenize
import multiprocessing


with open('key_api.txt', 'r') as f:
    auth_hdr_txt=f.readline()[:-1]

Auth_headers={'Authorization': 'Bearer ' + auth_hdr_txt }
base_url = 'http://api.genius.com'
artist_url = base_url + '/artists'
search_url = base_url + '/search'
songs_url = base_url + '/songs'

def lyrics_from_song_api_path(index, song_api_path):
    print(str(index))
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=Auth_headers)
    json = response.json()
    path = json['response']['song']['path']

    # Regular HTML scraping
    page_url = 'http://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find(class_='lyrics').get_text()
    return lyrics

def get_artist_api(artist_name):
    data = { 'q': artist_name }
    response = requests.get(search_url, params=data, headers=Auth_headers)
    json = response.json()
    artist_path = None
    for hit in json['response']['hits']:
        artist = hit['result']['primary_artist']
        if artist['name'] == artist_name:
            if artist['is_verified']:
                return artist['id'] # Prefer verified artists
            artist_path.append(artist['id'])
    if artist_path and len(artist_path):
        return artist_path[0]
    else:
        return None

def get_artist_songs(artist_id, nb_songs=100):
    page_num='1'
    songs_set = set()
    while page_num != 'None' and len(songs_set) < nb_songs:
        param = {'per_page': '50', 'page': page_num, 'sort': 'popularity'}
        response = requests.get(artist_url + '/' + str(artist_id) + '/songs',
                                params=param,
                                headers=Auth_headers)
        json = response.json()
        for song in json['response']['songs']:
            if len(songs_set) == nb_songs:
                break
            songs_set.add(song['api_path'])
        page_num = str(json['response']['next_page'])
    return list(songs_set)

def main(artist_name, nb_songs = 120):
    artist_api = get_artist_api(artist_name)
    artist_songs = get_artist_songs(artist_api, nb_songs)
    artist_lyrics=[]
    print('Counting')
    with multiprocessing.Pool(processes=20) as pool:
        lyrics = pool.starmap(lyrics_from_song_api_path,
                           enumerate(artist_songs))

    artist_lyrics = ''
    for i in lyrics:
        artist_lyrics += '--------------------------------------\n' + i + '\n'

    with open(artist_name + '.lyrics', 'w') as f:
        f.write(artist_lyrics)
    return artist_lyrics

if __name__ == '__main__':
    print('Starting')
    if (len(sys.argv) == 3):
        main(sys.argv[1], int(sys.argv[2]))
    elif (len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        print('Usage: ./generator.py ARTIST [NB_SONGS]')

import json
import urllib.parse

import requests
from bs4 import BeautifulSoup

URL = 'https://chordify.net/api/v2/songs/{}/chords?vocabulary=extended_inversions'


def get_page(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, 'html.parser')
    return None


def get_id_youtube(url):
    return str(url[url.index('?v=') + 3:])


HEADERS_MEGA = {
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://chordify.net",
    "referer": "https://chordify.net/",
}


def get_chordify(id):
    url = URL.format('youtube:' + str(id))
    req = requests.get(url, headers=HEADERS_MEGA)
    json_response = req.json()
    return json_response


def search_cifra(search):
    url = 'https://studiosolsolr-a.akamaihd.net/cc/h2/?q={}'
    url = url.format(urllib.parse.quote(search, safe=''))
    json_response = requests.get(url)
    result = json.loads(json_response.content[1:-2])
    return result


def get_notes(chordify_result, instrumento):
    items = chordify_result['chords'].split('\n')
    notes = [item.split(';')[1] for item in items if len(item.split(';')) > 2]
    array_notes = list(set([item for item in notes if item != 'N']))
    notes_result = []
    for note in array_notes:
        notes_result.append({
            'note': note,
            'image': get_image_note(note, instrumento)
        })
    return notes_result


URL_GUITAR = 'https://chordify.net/img/diagrams/guitar/{}.png'
URL_PIANO = 'https://chordify.net/img/diagrams/piano/{}.png'

map = {
    'Ds': 'Eb',
    'Gs': 'Ab',
    'As': 'Bb',
}


def get_image_note(note, type_instrument):
    notes_wrong = map.keys()
    note = str(note).replace(':', '_').replace('#', 's')
    for key in notes_wrong:
        if key in note:
            note = note.replace(key, map[key])
    if type_instrument == 'guitar':
        return URL_GUITAR.format(note)
    return URL_PIANO.format(note)

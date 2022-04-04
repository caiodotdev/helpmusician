import csv
import random
import string
from base64 import b64encode

import pyimgur
from appdirs import unicode
from django.db.models import (
    CharField,
    TextField,
    IntegerField,
    FloatField,
    EmailField,
    ForeignKey,
    FileField,
    DateTimeField,
    DateField,
    AutoField,
    BooleanField,
    ManyToManyField, ImageField
)
from django.forms.widgets import (
    Textarea,
    NumberInput,
    EmailInput,
    Select,
    TextInput,
    HiddenInput,
    CheckboxInput,
    CheckboxSelectMultiple,
)
from django.utils import timezone

from app.youtubedl import get_meta_info


def generate_random_string(n):
    """
    Generates a random string of length n
    :param n: Length of string
    :return: Random string
    """
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """
    CSV reader for UTF-8 documents
    :param unicode_csv_data: Data of CSV
    :param dialect: Dialect of CSV
    :param kwargs: Other args
    :return:
    """
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [str(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """
    UTF-8 Encoder
    :param unicode_csv_data:
    :return: Generator of UTF-8 encoding
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def field_to_widget(field):
    if type(field) is CharField:
        if field.choices:
            return Select(attrs={"class": "form-control"})
        return TextInput(attrs={"class": "form-control", "rows": 1})
    if type(field) is TextField:
        return Textarea(attrs={"class": "form-control", "rows": 5})
    if type(field) is AutoField:
        return HiddenInput(attrs={"class": "form-control", "rows": 1})
    if type(field) is IntegerField or type(field) is FloatField:
        return NumberInput(attrs={"class": "form-control"})
    if type(field) is EmailField:
        return EmailInput(attrs={"class": "form-control"})
    if type(field) is ForeignKey:
        return Select(attrs={"class": "form-control"})
    if type(field) is ManyToManyField:
        return CheckboxSelectMultiple(attrs={"class": ""},
                                      choices=((model.id, model) for model in field.related_model.objects.all()))
    if type(field) is BooleanField:
        return CheckboxInput(attrs={"class": ""})
    if type(field) is FileField:
        return TextInput(attrs={"class": "form-control fileinput", "type": "file"})
    if type(field) is ImageField:
        return TextInput(
            attrs={"class": "form-control imageinput", "type": "file", "accept": ".jpg, .jpeg, .png, .ico"})
    if type(field) is DateField:
        return TextInput(attrs={"class": "form-control datepicker date", "type": "date"})
    if type(field) is DateTimeField:
        return TextInput(attrs={"class": "form-control datetimepicker datetime", "type": "date"})
    if field.one_to_one:
        return Select(attrs={"class": "form-control"},
                      choices=((model.id, model) for model in field.related_model.objects.all()))

    return TextInput(attrs={"class": "form-control", "rows": 1})


def generate_bootstrap_widgets_for_all_fields(model):
    return {x.name: field_to_widget(x) for x in model._meta.get_fields()}


def upload_image(request, attribute='file'):
    """
    This method has upload file.
    """
    try:
        CLIENT_ID = "cdadf801dc167ab"
        data = b64encode(request.FILES[attribute].read())
        client = pyimgur.Imgur(CLIENT_ID)
        r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': data})
        return r['link']
    except (Exception,):
        return 'http://placehold.it/1024x800'


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; remove anything that is not an
    alphanumeric, dash, whitespace, comma, bracket, underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = text_to_id(s)
    s = remove_spaces(s)
    return re.sub(r'(?u)[^-\w\s.,[\]()]', '', s)


def remove_spaces(s):
    s = str(s).strip()
    s = str(s).replace(' ', '').replace(',', '_')
    return s


import re

import unicodedata


def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text


def get_artist_and_title(link):
    info = get_meta_info(link)
    url = info['url']
    # Parse artist and title info
    if info['embedded_artist'] and info['embedded_title']:
        # Embedded meta info takes precedence
        artist = info['embedded_artist']
        title = info['embedded_title']
    elif info['parsed_artist'] and info['parsed_title']:
        # Followed by parsing the artist and title from the video title
        artist = info['parsed_artist']
        title = info['parsed_title']
    else:
        # Followed by uploader name and video title
        artist = info['uploader']
        title = info['title']
    return artist, title, url


def save_dynamic_mix_copy(dynamic, dynamic_on_db):
    dynamic.status = 2
    dynamic.date_finished = timezone.now()
    dynamic.vocals_url = dynamic_on_db.vocals_url
    dynamic.vocals_path = dynamic_on_db.vocals_path
    dynamic.piano_url = dynamic_on_db.piano_url
    dynamic.piano_path = dynamic_on_db.piano_path
    dynamic.bass_url = dynamic_on_db.bass_url
    dynamic.bass_path = dynamic_on_db.bass_path
    dynamic.drums_url = dynamic_on_db.drums_url
    dynamic.drums_path = dynamic_on_db.drums_path
    dynamic.other_url = dynamic_on_db.other_url
    dynamic.other_path = dynamic_on_db.other_path
    dynamic.folder_path_on_dropbox = dynamic_on_db.folder_path_on_dropbox
    dynamic.save()

# import pafy
from youtubesearchpython import VideosSearch


def get_youtube_search(music_name):
    videosSearch = VideosSearch(music_name, limit=25)
    return videosSearch.result()


def make_youtube_url(id):
    return 'https://www.youtube.com/watch?v=' + str(id)

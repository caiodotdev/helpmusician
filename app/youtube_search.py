from youtube_title_parse import get_artist_title

from youtubesearchpython import VideosSearch

"""
This module handles YouTube search API functionality.
"""


class YouTubeSearchError(Exception):
    pass


# def duration_is_valid(duration):
#     dur = datetime.datetime.strptime(str(duration), '%M:%S')
#     print(dur)
#     max_dur = datetime.datetime.strptime('08:30', '%M:%S')
#     return dur <= max_dur


def perform_search(query: str, page_token=None):
    videosSearch = VideosSearch(query, limit=25)
    search_items = videosSearch.result()['result']

    # Merge results into single, simplified list
    videos = []
    for item in search_items:
        if item['type'] == 'video':
            # if item['type'] == 'video' and duration_is_valid(item['duration']):
            result = get_artist_title(item['title'])

            if result:
                parsed_artist, parsed_title = result
            else:
                parsed_artist = item['channel']['name']
                parsed_title = item['title']

            videos.append(
                {
                    'id': item['id'],
                    'title': item['title'],
                    'parsed_artist': parsed_artist,
                    'parsed_title': parsed_title,
                    'channel': item['channel']['name'],
                    'thumbnail': item['thumbnails'][0]['url'],
                    'duration': item['duration']
                }
            )

    next_page_token = None
    # Return next page token and video result
    return next_page_token, videos

# import pafy
from youtubesearchpython import VideosSearch
from django.template.defaultfilters import filesizeformat


def get_youtube_search(music_name):
    videosSearch = VideosSearch(music_name, limit=12)
    return videosSearch.result()


def make_youtube_url(id):
    return 'https://www.youtube.com/watch?v=' + str(id)


# def download_video(url_video):
#     video = pafy.new(url_video)
#     stream = video.streams
#     video_audio_streams = []
#     for s in stream:
#         video_audio_streams.append({
#             'resolution': s.resolution,
#             'extension': s.extension,
#             'file_size': filesizeformat(s.get_filesize()),
#             'video_url': s.url + "&title=" + video.title
#         })
#
#     stream_audio = video.audiostreams
#     audio_streams = []
#     for s in stream_audio:
#         audio_streams.append({
#             'resolution': s.resolution,
#             'extension': s.extension,
#             'file_size': filesizeformat(s.get_filesize()),
#             'video_url': s.url + "&title=" + video.title
#         })
#     return video_audio_streams, audio_streams

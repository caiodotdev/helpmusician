from sys import platform

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from youtube_title_parse import get_artist_title
from youtubesearchpython import VideosSearch

from app.custom_mixin import CustomTemplateView, CustomContextMixin
from app.middleware import UnauthorizedException
from app.requests_api import _do_get, _do_post, _do_delete, _do_patch, _do_put
from .serializers import *

"""
This module defines Django views.
"""

SERVER_URL = settings.SERVER_URL
# Windows users would need to use Celery with 'gevent', but 'gevent' does not support aborting in-progress tasks,
# so the SIGTERM would still fail...
KILL_SIGNAL = 'SIGTERM' if platform == 'win32' else 'SIGUSR1'


class IndexView(CustomContextMixin, CustomTemplateView):
    template_name = 'index.html'


class MixerView(CustomContextMixin, CustomTemplateView):
    template_name = 'index.html'


class YouTubeSearchView(APIView):
    """View that processes YouTube video search queries."""

    # TODO: Add check_authentication in method

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        serializer = YTSearchQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return JsonResponse(
                {
                    'status': 'error',
                    'errors': ['Invalid YouTube search query']
                },
                status=400)
        data = serializer.validated_data
        query = data['query']
        videosSearch = VideosSearch(query, limit=10)
        search_items = videosSearch.result()['result']

        # Merge results into single, simplified list
        videos = []
        for item in search_items:
            if item['type'] == 'video':
                parsed_artist = None
                parsed_title = None
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
        return JsonResponse({
            'next_page_token': None,
            'results': videos
        })


class YTLinkInfoView(CustomContextMixin, APIView):

    # TODO: Add check_authentication in method

    def get(self, request):
        context = self.get_context_data()
        token = context['token']
        req = _do_get(SERVER_URL + '/api/source-file/youtube/', request.GET, token)
        return JsonResponse(data=req.json())


class SourceFileListView(CustomContextMixin, generics.ListAPIView):
    """View that returns list of all SourceFiles."""
    queryset = SourceFile.objects.all()
    serializer_class = SourceFileSerializer

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        token = context['token']
        req = _do_get(SERVER_URL + '/api/source-file/all/', request.GET, token)
        return JsonResponse(data=req.json())


class SourceFileView(CustomContextMixin, viewsets.ModelViewSet):
    """View that handles SourceFile creation and deletion."""
    queryset = SourceFile.objects.all()
    serializer_class = SourceFileSerializer

    def create(self, request, *args, **kwargs):
        """Handle request to create a SourceFile (i.e. user uploads a new audio file.)"""
        data = self.request.data
        tf = data['file']
        chunk = ' '
        while len(chunk) > 0:
            chunk = request.read(1024)
            tf.write(chunk)
        tf.seek(0)
        del data['file']
        context = self.get_context_data()
        token = context['token']
        req = _do_post(SERVER_URL + '/api/source-file/file/', data=data, token=token, verify=True, files={"file": tf})
        return JsonResponse(data=req.json())

    def perform_destroy(self, request):
        """Handle request to delete a SourceFile (i.e. user cancels upload operation)"""
        context = self.get_context_data()
        token = context['token']
        # TODO: check if other results 401 404 400
        req = _do_delete(SERVER_URL + '/api/source-file/file/', token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SourceTrackRetrieveUpdateDestroyView(CustomContextMixin, generics.RetrieveUpdateDestroyAPIView):
    """View that handles SourceTrack deletion and retrieval."""
    queryset = SourceTrack.objects.all()
    serializer_class = LiteSourceTrackSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_get(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.GET, token=token)
        return JsonResponse(data=req.json())

    def patch(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_patch(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.PATCH, token=token)
        return JsonResponse(data=req.json())

    def put(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_put(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.PUT, token=token)
        return JsonResponse(data=req.json())

    def delete(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_delete(SERVER_URL + '/api/source-track/{}/'.format(uuid), token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SourceTrackListView(CustomContextMixin, generics.ListAPIView):
    """View that handles listing SourceTracks."""
    # queryset = SourceTrack.objects.all()
    serializer_class = LiteSourceTrackSerializer

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        token = context['token']
        data = request.GET.copy()
        data['user'] = context['user_data']['id']
        req = _do_get(SERVER_URL + '/api/source-track/', data, token, data)
        return JsonResponse(data=req.json(), safe=False)


class FileSourceTrackView(CustomContextMixin, generics.CreateAPIView):
    """View that handles SourceTrack creation from user-uploaded files."""
    serializer_class = FullSourceTrackSerializer

    def create(self, request, *args, **kwargs):
        context = self.get_context_data()
        token = context['token']
        req = _do_post(SERVER_URL + '/api/source-track/file/', data=self.request.data, token=token)
        return JsonResponse(data=req.json())


class YTSourceTrackView(CustomContextMixin, generics.CreateAPIView):
    """View that handles SourceTrack creation from user-imported YouTube links."""
    queryset = SourceTrack.objects.all()
    serializer_class = YTSourceTrackSerializer

    def create(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not 'user_data' in context:
            raise UnauthorizedException()
        token = context['token']
        data = self.request.data
        data['user'] = context['user_data']['id']
        req = _do_post(SERVER_URL + '/api/source-track/youtube/', data=data, token=token)
        return JsonResponse(data=req.json())


class DynamicMixCreateView(CustomContextMixin, generics.ListCreateAPIView):
    """View that handles creating a DynamicMix instance."""
    serializer_class = FullDynamicMixSerializer
    queryset = DynamicMix.objects.all()

    def create(self, request, *args, **kwargs):
        context = self.get_context_data()
        token = context['token']
        req = _do_post(SERVER_URL + '/api/mix/dynamic/', data=request.data, token=token)
        return JsonResponse(data=req.json())


class DynamicMixRetrieveDestroyView(CustomContextMixin, generics.RetrieveDestroyAPIView):
    """View for handling DynamicMix lookup by ID."""
    serializer_class = LiteDynamicMixSerializer
    queryset = DynamicMix.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_get(SERVER_URL + '/api/mix/dynamic/{}/'.format(uuid), data=request.data, token=token)
        return JsonResponse(data=req.json())

    def delete(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_delete(SERVER_URL + '/api/mix/dynamic/{}/'.format(uuid), token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaticMixCreateView(CustomContextMixin, generics.ListCreateAPIView):
    """View that handles creating StaticMix"""
    serializer_class = FullStaticMixSerializer
    queryset = StaticMix.objects.all()

    def create(self, request, *args, **kwargs):
        context = self.get_context_data()
        token = context['token']
        req = _do_post(SERVER_URL + '/api/mix/static/', data=self.request.data, token=token)
        return JsonResponse(data=req.json())


class StaticMixRetrieveDestroyView(CustomContextMixin, generics.RetrieveDestroyAPIView):
    """View for handling StaticMix deletion and retrieval."""
    serializer_class = LiteStaticMixSerializer
    queryset = StaticMix.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_get(SERVER_URL + '/api/mix/static/{}/'.format(uuid), data=request.data, token=token)
        return JsonResponse(data=req.json())

    def delete(self, request, *args, **kwargs):
        uuid = str(self.kwargs['id'])
        context = self.get_context_data()
        token = context['token']
        req = _do_delete(SERVER_URL + '/api/mix/static/{}/'.format(uuid), token=token)
        return Response(status=status.HTTP_204_NO_CONTENT)


class YTAudioDownloadTaskRetrieveView(generics.RetrieveAPIView):
    """View for handling YTAudioDownloadTask lookup by ID."""
    serializer_class = YTAudioDownloadTaskSerializer
    queryset = YTAudioDownloadTask.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        req = requests.get(SERVER_URL + '/api/task/{}/'.format(uuid), data=request.GET)
        return JsonResponse(data=req.json())


class YTAudioDownloadTaskListView(generics.ListAPIView):
    """View that handles listing YouTube download tasks."""
    queryset = YTAudioDownloadTask.objects.all()
    serializer_class = YTAudioDownloadTaskSerializer

    def get(self, request, *args, **kwargs):
        req = requests.get(SERVER_URL + '/api/task/', data=request.GET)
        return JsonResponse(data=req.json())

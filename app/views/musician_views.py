from sys import platform

import django_filters
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from app.celery import app
from django.contrib import messages
from django.contrib.admin.utils import NestedObjects
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, FormView
from youtube_title_parse import get_artist_title

from app.apis.DetectMobile import DetectMobileBrowser
from app.apis.chordify import get_chordify, get_id_youtube, get_notes
from app.apis.youtube import get_youtube_search, make_youtube_url
from app.forms import SourceTrackForm, UploadForm
from app.models import DynamicMix, SourceFile, YTAudioDownloadTask, SourceTrack, TaskStatus
from app.tasks import create_dynamic_mix, fetch_youtube_audio, fetch_upload_audio
from app.utils import get_valid_filename

KILL_SIGNAL = 'SIGTERM' if platform == 'win32' else 'SIGUSR1'


class TrackFilter(django_filters.FilterSet):
    class Meta:
        model = SourceTrack
        fields = ["artist", "title", "tone", "bpm", ]


class ListTracks(LoginRequiredMixin, ListView):
    """
    List all Channels
    """
    login_url = '/login/'
    template_name = 'music/list.html'
    model = SourceTrack
    ordering = '-id'
    context_object_name = 'tracks'
    paginate_by = 10
    search = ''

    def get_queryset(self):
        qs = SourceTrack.objects.filter(user=self.request.user)
        filter = TrackFilter(self.request.GET, qs)
        queryset = self.search_general(filter.qs)
        queryset = self.ordering_data(queryset)
        return queryset

    def search_general(self, qs):
        if 'search' in self.request.GET:
            self.search = self.request.GET['search']
            if self.search:
                search = self.search
                qs = qs.filter(Q(id__icontains=search) | Q(title__icontains=search) |
                               Q(artist__icontains=search) | Q(tone__icontains=search) | Q(bpm__icontains=search))
        return qs

    def get_ordering(self):
        if 'ordering' in self.request.GET:
            self.ordering = self.request.GET['ordering']
            if self.ordering:
                return self.ordering
            else:
                self.ordering = '-id'
        return self.ordering

    def ordering_data(self, qs):
        qs = qs.order_by(self.get_ordering())
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListTracks, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = TrackFilter(self.request.GET, queryset)
        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context.update(**{
                'ordering': self.ordering,
                'search': self.search,
                'filter': filter,
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            })
        else:
            context.update(**{
                'search': self.search,
                'ordering': self.ordering,
                'filter': filter,
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            })
        return context


class ResultsView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'music/results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResultsView, self).get_context_data()
        data = self.request.GET
        if 'search' in data:
            musica = data['search']
            results = get_youtube_search(musica)
            context['results'] = results['result']
            return context
        else:
            messages.error(self.request, 'Digite alguma musica')
            return reverse('index')


class ConfirmMusic(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = SourceTrack
    form_class = SourceTrackForm
    template_name = 'music/confirm_music.html'
    success_url = '/'

    def get_initial(self):
        return {
            'user': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super(ConfirmMusic, self).get_context_data()
        data = self.request.GET
        if 'id' in data:
            id_video = data['id']
            youtube_link = make_youtube_url(id_video)
            if get_artist_title(data['title']):
                artist, title = get_artist_title(data['title'])
            else:
                artist = ''
                title = ''
            youtube_link = make_youtube_url(data['id'])
            context['id'] = data['id']
            context['thumb'] = data['thumb']
            context['artist'] = artist
            context['title'] = title
            context['youtube_link'] = youtube_link
        return context

    def save_chordify_on_track(self, data, source_track):
        try:
            result_chordify = get_chordify(get_id_youtube(data['youtube_link']))
            source_track.notes = str(get_notes(result_chordify, 'guitar'))
            source_track.tone = result_chordify['derivedKey']
            source_track.bpm = result_chordify['derivedBpm']
            source_track.bar_length = result_chordify['barLength']
            source_track.chords = result_chordify['chords']
            source_track.save()
        except (Exception,):
            print('Nao foi possivel salvar chordify para esta track')

    def form_valid(self, form):
        data = form.cleaned_data
        data['youtube_link'] = self.request.POST['youtube_link']
        try:
            qs = SourceFile.objects.filter(youtube_link=data['youtube_link'])
            if not qs.exists():
                fetch_task = YTAudioDownloadTask()
                fetch_task.save()
                source_file = SourceFile(is_youtube=True,
                                         youtube_link=data['youtube_link'],
                                         youtube_fetch_task=fetch_task)
                source_file.save()
                source_track = form.save()
                custom_data = self.request.POST
                source_track.artist = custom_data['artist']
                source_track.title = custom_data['title']
                source_track.thumb = custom_data['thumb']
                source_track.source_file = source_file
                source_track.save()
                try:
                    # Kick off download task in background
                    artist = str(get_valid_filename(custom_data['artist'])).strip()
                    title = str(get_valid_filename(custom_data['title'])).strip()
                    result = fetch_youtube_audio.delay(source_file.id, source_track.id, fetch_task.id,
                                                       artist, title,
                                                       custom_data['youtube_link'])
                    # Set the celery task ID in the model
                    YTAudioDownloadTask.objects.filter(id=fetch_task.id).update(
                        celery_id=result.id)
                except Exception as error:
                    print(error)
            else:
                source_file = qs.first()
                source_track_copy = source_file.sourcetrack_set.first()
                source_track = form.save()
                source_track.artist = source_track_copy.artist
                source_track.title = source_track_copy.title
                source_track.thumb = source_track_copy.thumb
                source_track.source_file = source_file
                source_track.save()
                create_dynamic_mix(source_track)
            self.save_chordify_on_track(data, source_track)
            messages.success(self.request, 'Estamos baixando sua música, aguarde.')
            return super(ConfirmMusic, self).form_valid(form)
        except (Exception,):
            messages.error(self.request, 'Erro Desconhecido, tente mais tarde.')
            return super(ConfirmMusic, self).form_invalid(form)

    def get_success_url(self):
        return '/'


class CustomMixer(LoginRequiredMixin, DetectMobileBrowser, DetailView):
    login_url = '/login/'
    template_name = 'kits/custom_mixer.html'
    model = DynamicMix
    context_object_name = 'data'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        return DynamicMix.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = {}
        self.object = self.get_object()
        dynamic = self.object
        kwargs['chords'] = [clause.split(';') for clause in dynamic.source_track.chords.split('\n')]
        context.update(kwargs)
        return super(CustomMixer, self).get_context_data(**context)


class PlayerView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = SourceTrack
    template_name = 'music/player.html'
    context_object_name = 'track'
    pk_url_kwarg = 'id'
    success_url = '/'

    def get_object(self, queryset=None):
        return SourceTrack.objects.get(id=self.kwargs['id'])


class DeleteDynamic(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = DynamicMix
    template_name = 'music/delete.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'id'
    success_url = '/'

    def get_object(self, queryset=None):
        return DynamicMix.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(DeleteDynamic, self).get_context_data(**kwargs)
        collector = NestedObjects(using='default')
        collector.collect([self.get_object()])
        context['deleted_objects'] = collector.nested()
        return context

    def delete(self, request, *args, **kwargs):
        dynamic_mix = self.get_object()
        celery_id = dynamic_mix.celery_id
        print('Revoking celery task:', celery_id)
        app.control.revoke(celery_id, terminate=True, signal=KILL_SIGNAL)
        messages.success(self.request, 'Mix removida com sucesso')
        dynamic_mix.source_track.delete()

        if dynamic_mix.source_track is not None and not dynamic_mix.source_track.url() and dynamic_mix.source_track.source_file.is_youtube:
            # Empty URL
            celery_id = dynamic_mix.source_track.source_file.youtube_fetch_task.celery_id
            print('Revoking celery task:', celery_id)
            app.control.revoke(celery_id, terminate=True, signal=KILL_SIGNAL)

        pending_dynamic_mixes = DynamicMix.objects.filter(
            Q(source_track=dynamic_mix.source_track)
            & (Q(status=TaskStatus.IN_PROGRESS)
               | Q(status=TaskStatus.QUEUED)))

        for dynamic_mix in pending_dynamic_mixes:
            celery_id = dynamic_mix.celery_id
            print('Revoking celery task:', celery_id)
            app.control.revoke(celery_id, terminate=True, signal=KILL_SIGNAL)
        return HttpResponseRedirect(self.success_url)


class DrumKit(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'kits/drumkit.html'


class PadContinuous(LoginRequiredMixin, DetectMobileBrowser, TemplateView):
    login_url = '/login/'
    template_name = 'kits/pad_continuous.html'


class SelectedView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'music/selected.html'
    model = SourceTrack
    queryset = SourceTrack.objects.filter(user__username='caiomarinho')
    context_object_name = 'tracks'


class SelectedOut(ListView):
    template_name = 'music/selected_out.html'
    model = SourceTrack
    queryset = SourceTrack.objects.filter(user__username='caiomarinho')
    context_object_name = 'tracks'


class ConfirmAddMusic(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = SourceTrack
    form_class = SourceTrackForm
    template_name = 'music/confirm_music.html'
    success_url = '/'

    def get_initial(self):
        return {
            'user': self.request.user,
        }

    def get_context_data(self, **kwargs):
        context = super(ConfirmAddMusic, self).get_context_data()
        data = self.request.GET
        if 'link' in data:
            context['artist'] = data['artist']
            context['title'] = data['title']
            context['thumb'] = data['thumb']
            context['youtube_link'] = data['link']
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        data['youtube_link'] = self.request.POST['youtube_link']
        try:
            qs = SourceFile.objects.filter(youtube_link=data['youtube_link'])
            source_file = qs.first()
            source_track_copy = source_file.sourcetrack_set.first()
            source_track = form.save()
            source_track.artist = self.request.POST['artist']
            source_track.title = self.request.POST['title']
            source_track.thumb = source_track_copy.thumb
            source_track.source_file = source_file
            source_track.notes = source_track_copy.notes
            source_track.tone = source_track_copy.tone
            source_track.bpm = source_track_copy.bpm
            source_track.bar_length = source_track_copy.bar_length
            source_track.chords = source_track_copy.chords
            source_track.save()
            create_dynamic_mix(source_track)
            messages.success(self.request, 'Música adicionada com sucesso.')
            return super(ConfirmAddMusic, self).form_valid(form)
        except (Exception,):
            messages.error(self.request, 'Erro Desconhecido, tente mais tarde.')
            return super(ConfirmAddMusic, self).form_invalid(form)

    def get_success_url(self):
        return '/'

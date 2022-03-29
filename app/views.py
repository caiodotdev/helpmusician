#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http
import json

import requests
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.generic.edit import (
    FormView
)
from django.views.generic.list import ListView
from rest_framework import status
from youtube_title_parse import get_artist_title

from app import requests_api
from app.apis.chordify import get_chordify, get_notes
from app.apis.youtube import get_youtube_search, make_youtube_url
from app.custom_mixin import CustomFormView, CustomContextMixin
from app.models import Music
from app.requests_api import _do_post

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy, reverse

from app.forms import SearchForm, ArtistForm, NewUserForm, LoginForm


class SearchTemplate(CustomContextMixin, CustomFormView):
    form_class = SearchForm
    template_name = 'music/search.html'

    def get_success_url(self):
        data = self.request.POST
        if 'musica' in data:
            musica = data['musica']
            return '/results/' + '?musica=' + str(musica)
        return ''


class ResultsView(CustomContextMixin, ListView):
    model = Music
    login_url = '/admin/login/'
    context_object_name = 'musics'
    ordering = '-id'
    paginate_by = 1
    template_name = 'music/results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResultsView, self).get_context_data()
        data = self.request.GET
        if 'musica' in data:
            musica = data['musica']
            results = get_youtube_search(musica)
            context['results'] = results['result']
            return context
        raise Http404()


class ConfirmMusic(CustomContextMixin, FormView):
    form_class = ArtistForm
    template_name = 'music/confirm_music.html'

    def get_context_data(self, **kwargs):
        context = super(ConfirmMusic, self).get_context_data()
        if 'id' in self.request.GET:
            data = self.request.GET
            id_video = data['id']
            youtube_link = make_youtube_url(id_video)
            context['id'] = id_video
            info = get_artist_title(data['title'])
            if info:
                artist, title = info
                context['artist'] = artist
                context['title'] = title
            context['image'] = data['thumb']
            context['youtube_link'] = youtube_link
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        data['youtube_link'] = self.request.POST['youtube_link']
        data['user'] = self.get_context_data()['user_data']['id']
        req = _do_post(settings.SERVER_URL + '/api/source-track/youtube/', data,
                       requests_api.get_token(self.request))
        if req.status_code == status.HTTP_200_OK:
            return super(ConfirmMusic, self).form_valid(form)
        elif req.status_code == status.HTTP_400_BAD_REQUEST:
            messages.error(self.request, str(req.json()['errors'][0]))
            return super(ConfirmMusic, self).form_invalid(form)
        else:
            messages.error(self.request, 'Erro Desconhecido, tente mais tarde.')
            return super(ConfirmMusic, self).form_invalid(form)

    def get_success_url(self):
        return '/lista/'


class VideoView(CustomContextMixin, TemplateView):
    login_url = '/admin/login/'
    template_name = 'music/video.html'
    instrumento = 'guitar'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoView, self).get_context_data()
        if 'instrumento' in self.request.GET:
            data = self.request.GET
            instrumento = data['instrumento']
        else:
            instrumento = 'guitar'
        data = self.request.GET
        if 'id' in data:
            id_video = data['id']
            url_youtube_video = make_youtube_url(id_video)
            chordify_result = get_chordify(id_video)
            context['id'] = id_video
            context['notes'] = get_notes(chordify_result, instrumento)
            context['title'] = data['title']
            context['result'] = chordify_result
            context['url_video'] = url_youtube_video
            # streams, stream_audio = download_video(url_youtube_video)
            # context['streams'] = streams
            # context['stream_audio'] = stream_audio
            return context
        raise Http404()


class RegisterView(FormView):
    template_name = 'account/signup.html'
    form_class = NewUserForm
    success_url = '/'

    def form_valid(self, form):
        req = requests_api.do_register(data=form.cleaned_data)
        if req.status_code == http.HTTPStatus.OK:
            print(req.json())
            messages.success(self.request, "Usuario registrado com sucesso.")
        else:
            messages.error(self.request, "Nao foi possivel registrar. Altere os dados e tente novamente.")
            return self.form_invalid(form)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Nao foi possivel registrar. Altere os dados e tente novamente.")
        return super(RegisterView, self).form_invalid(form)


class LoginView(FormView):
    """
    Displays the login form.
    """

    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = '/'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return "%s" % next_url
        else:
            return reverse('index')

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL if login is successful.
        """
        data = form.cleaned_data
        try:
            response = requests_api.do_login(data['username'], data['password'])
            if response.status_code == http.HTTPStatus.OK:
                requests_api.save_all_data(self.request, response)
                return super(LoginView, self).form_valid(form)
            else:
                messages.error(self.request, 'Credenciais invalidas, Tente novamente')
        except requests.exceptions.RequestException:
            messages.error(self.request, 'Erro de autenticação, tente novamente mais tarde')
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario ou senha invalidos.')
        return super(LoginView, self).form_invalid(form)


@require_http_methods(["GET"])
def logout_user(request):
    """
    User make logout.
    """
    requests_api.session_clear(request)
    requests_api.do_logout(request)
    return redirect('login')

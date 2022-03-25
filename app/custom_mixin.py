# -*- coding: utf-8 -*-

"""
Xingu mixin controller.
"""

from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.template import loader
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import ProcessFormView, FormView

from app import requests_api
from app.middleware import UnauthorizedException


class CustomTemplateView(TemplateView):
    """
    Implements method to get default template.
    """

    def get(self, request, *args, **kwargs):
        auth = check_authorization(self.request)
        if auth:
            return auth
        return super(CustomTemplateView, self).get(request, *args, **kwargs)


class CustomFormView(FormView):
    """
    Implements method to get default form.
    """

    def get(self, request, *args, **kwargs):
        auth = check_authorization(self.request)
        if auth:
            return auth
        return super(CustomFormView, self).get(request, *args, **kwargs)


class CustomContextMixin(ContextMixin):
    """
    Implements method to get default context.
    """

    def get_context_data(self, **kwargs):
        """
        This method initiates the context default.
        """

        context = super(CustomContextMixin, self).get_context_data(**kwargs)

        for msg in get_messages(self.request):
            if msg.level == messages.ERROR:
                context['error'] = msg.message
            elif msg.level == messages.SUCCESS:
                context['message'] = msg.message
        try:
            context['token'] = self.request.session['token']
            context['user_data'] = self.request.session['user_data']
        except (Exception,):
            raise UnauthorizedException()
        return context


def check_authorization(request):
    """
    This function checks if user was logged.
    """
    if not requests_api.has_user_session(request):
        # messages.error(request, 'Não Autorizado, por favor, faça Login')
        return redirect('/login/?next=%s' % request.path)

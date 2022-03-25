# -*- coding: utf-8 -*-

"""
Middleware classes used in request/response processing.
See: https://docs.djangoproject.com/en/1.8/topics/http/middleware/
"""
from django.contrib import messages
from django.shortcuts import redirect

__copyright__ = 'Copyright (c) TPV 2015. All rights reserved.'

from django.utils.deprecation import MiddlewareMixin


class UnauthorizedException(Exception):
    """
    Handles unauthorized exceptions.
    """


class ForbiddenException(Exception):
    """
    Handles forbidden exceptions.
    """


class CustomMiddleware(MiddlewareMixin):
    """
    Handles request/response processing.
    """

    @classmethod
    def process_exception(cls, request, exception):
        """
        Handle exceptions raised by views.
        :param request: HttpRequest object.
        :param exception: Exception object raised by the view function.
        :return: The HttpResponse handling the exception or None if no action is taken.
        """
        response = None
        if isinstance(exception, UnauthorizedException):
            if request.session.get('user_data'):
                messages.error(request, 'Sua sessão expirou')
            response = redirect('login')
        elif isinstance(exception, ForbiddenException):
            if request.session.get('user_data'):
                messages.error(request, 'Permissão Negada')
            response = redirect('index')
        return response

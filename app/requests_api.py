import http
import json

import requests

from django.conf import settings

from app.middleware import UnauthorizedException

URL_LOGIN = settings.SERVER_URL + '/api/login/'
URL_USERS = settings.SERVER_URL + '/api/user/'
URL_LOGOUT = settings.SERVER_URL + '/api/logout/'
URL_REGISTER = settings.SERVER_URL + '/api/register/'


def _do_post(url, data, token=None, verify=True, files=None):
    """
    Sends a POST request.
    :param url: Target URL.
    :param data: POST data.
    :param token: Authentication token.
    :return: Request response.
    """
    headers = {'content-type': 'application/json'}
    if token:
        headers['Authorization'] = 'Token ' + token
    if files:
        response = requests.post(url, data=json.dumps(data), headers=headers, files=files, verify=verify)
    else:
        response = requests.post(url, data=json.dumps(data), headers=headers, verify=verify)
    if response.status_code == http.HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedException()
    return response


def _do_put(url, data, token, verify=True):
    """
    Sends a PUT request.
    :param url: Target URL.
    :param data: PUT data.
    :param token: Authentication token.
    :return: Request response.
    """
    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + token}
    response = requests.put(url, data=json.dumps(data), headers=headers, verify=verify)
    if response.status_code == http.HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedException()
    return response


def _do_patch(url, data, token, verify=True):
    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + token}
    response = requests.patch(url, data=json.dumps(data), headers=headers, verify=verify)
    if response.status_code == http.HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedException()
    return response


def _do_get(url, data, token, params=None, verify=True):
    """
    Sends a GET request.
    :param url: Target URL.
    :param token: Authentication token.
    :return: Request response.
    """
    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + token}
    try:
        if params:
            response = requests.get(url, headers=headers, data=json.dumps(data), params=params, verify=verify)
        else:
            response = requests.get(url, headers=headers, verify=verify)
        return response
    except requests.RequestException:
        raise UnauthorizedException()


def _do_delete(url, token):
    """
    Sends a DELETE request.
    :param url: Target URL.
    :param token: Authentication token.
    :return: Request response.
    """
    headers = {'content-type': 'application/json', 'Authorization': 'Token ' + token}
    response = requests.delete(url, headers=headers, verify=False)
    if response.status_code == http.HTTPStatus.UNAUTHORIZED:
        raise UnauthorizedException()
    return response


def get_token(request):
    """
    This method takes the TOKEN in request after login.
    :param request: a request after login.
    :return: a token string.
    """
    try:
        token = request.session['token']
    except KeyError:
        token = "InvalidToken"
    return token


def get_user_request(token, id_user):
    """
    This method get a user data by id.
    :param token: a current token user.
    :param id_user: user id.
    :return: a response.
    """
    return _do_get(URL_USERS + str(id_user) + '/', None, token)


def get_current_user(request):
    """
    This method takes the USER DATA in request after login.
    :param request: a request after login.
    :return: a user data json.
    """
    response = get_user_request(get_token(request), request.session['user_data']['id'])
    return response.json()


def get_perms(request):
    """
    This method takes the USER PERMISSIONS in request after login.
    :param request: a request after login.
    :return: a user permissions data.
    """
    return request.session['perms']


def save_data_session(request, key, value):
    """
    This is method save content data in session.
    :param request: a current request.
    :param key: a key.
    :param value: a content data.
    """
    # Saving profile_id value
    # if isinstance(value, dict) and 'id' not in value:
    #     value['id'] = request.session['' + key]['id']
    request.session['' + key] = value


def save_token(request, token):
    """
    This method save token in session after login.
    :param request: a current request.
    :param token: the token generated from webservice.
    """
    save_data_session(request, 'token', token)


def save_expiry(request, expiry):
    save_data_session(request, 'expiry', expiry)


def save_user(request, user):
    """
    This method save user data in session after login.
    :param request: a current request.
    :param user: a user data.
    """
    save_data_session(request, 'user_data', user)


def save_perms(request, perms):
    """
    This method save user permissions in session after login.
    :param request: a current request.
    :param perms: a permissions data.
    """
    save_data_session(request, 'perms', perms)


def session_clear(request):
    """
    This method clear the session.
    :param request: a current request.
    """
    request.session.clear_expired()
    request.session.clear()
    request.session.flush()


def has_user_session(request):
    """
    Verifies if an user session exists.
    :param request: a current request.
    :return: a boolean result.
    """
    try:
        resp = _do_get(URL_USERS, None, get_token(request))
        if resp.status_code == http.HTTPStatus.OK:
            return True
    except UnauthorizedException:
        return False


def save_all_data(request, data):
    """
    This method save all content in session after login request.
    :param request: a login response.
    :param data: a full data.
    """
    data = data.json()
    save_token(request, data['token'])
    save_expiry(request, data['expiry'])
    # save_perms(request, data.json()['perms'])
    user_data = data['user']
    # user_data['profile'] = user_data.pop('profileName')
    save_user(request, user_data)


def do_login(username, password):
    """
    This method do login.
    :param email: a user email.
    :param password: a user password.
    :return: if status code 200, return a request with permissions and
    token (need convert to json).
    """
    payload = {'username': username, 'password': password}
    try:
        response = _do_post(URL_LOGIN, data=payload)
    except UnauthorizedException:
        response = type('Response', (object,), dict(status_code=http.HTTPStatus.UNAUTHORIZED))
    return response


def do_register(data):
    try:
        response = _do_post(URL_REGISTER, data, None)
    except UnauthorizedException:
        response = type('Response', (object,), dict(status_code=http.HTTPStatus.UNAUTHORIZED))
    return response


def do_logout(request):
    try:
        token = get_token(request)
        response = _do_get(URL_LOGOUT, None, token)
    except UnauthorizedException:
        response = type('Response', (object,), dict(status_code=http.HTTPStatus.UNAUTHORIZED))
    return response

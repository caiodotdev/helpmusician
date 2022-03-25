import requests
from django.http import JsonResponse
from django.shortcuts import render

SERVER_URL = 'http://localhost:8000'


def index(request):
    return render(request, 'index.html')


def youtube_search_view(request):
    req = requests.get(SERVER_URL + '/api/search/', data=request.GET)
    return JsonResponse(data=req.json())


# not used on frontend
def source_file_list_view(request):
    req = requests.get(SERVER_URL + '/api/source-file/all/', data=request.GET)
    return JsonResponse(data=req.json())


def source_file_view(request):
    if request.POST:
        req = requests.post(SERVER_URL + '/api/source-file/file/', data=request.POST)
    else:
        req = requests.delete(SERVER_URL + '/api/source-file/file/', data=request.DELETE)
    return JsonResponse(data=req.json())


def youtube_link_info_view(request):
    req = requests.get(SERVER_URL + '/api/source-file/youtube/', data=request.GET)
    return JsonResponse(data=req.json())


def source_track_list(request):
    req = requests.get(SERVER_URL + '/api/source-track/', data=request.GET)
    return JsonResponse(data=req.json())


def source_track_crud(request, uuid):
    if request.PATCH:
        req = requests.patch(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.PATCH)
    elif request.DELETE:
        req = requests.delete(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.DELETE)
    else:
        req = requests.get(SERVER_URL + '/api/source-track/{}/'.format(uuid), data=request.GET)
    return JsonResponse(data=req.json())


def file_source_track_view(request):
    req = requests.post(SERVER_URL + '/api/source-track/file/', data=request.POST)
    return JsonResponse(data=req.json())


def youtube_source_track_view(request):
    req = requests.post(SERVER_URL + '/api/source-track/youtube/', data=request.POST)
    return JsonResponse(data=req.json())


def staticmix_create(request):
    req = requests.post(SERVER_URL + '/api/mix/static/', data=request.POST)
    return JsonResponse(data=req.json())


def staticmix_crud(request, uuid):
    if request.DELETE:
        req = requests.delete(SERVER_URL + '/api/mix/static/{}/'.format(uuid), data=request.DELETE)
    else:
        req = requests.get(SERVER_URL + '/api/mix/static/{}/'.format(uuid), data=request.GET)
    return JsonResponse(data=req.json())


def dynamicmix_create(request):
    req = requests.post(SERVER_URL + '/api/mix/dynamic/', data=request.POST)
    return JsonResponse(data=req.json())


def dynamicmix_crud(request, uuid):
    if request.DELETE:
        req = requests.delete(SERVER_URL + '/api/mix/dynamic/{}/'.format(uuid), data=request.DELETE)
    else:
        req = requests.get(SERVER_URL + '/api/mix/static/{}/'.format(uuid), data=request.GET)
    return JsonResponse(data=req.json())


def task_create(request):
    req = requests.post(SERVER_URL + '/api/task/', data=request.POST)
    return JsonResponse(data=req.json())


def task_crud(request, uuid):
    if request.DELETE:
        req = requests.delete(SERVER_URL + '/api/task/{}/'.format(uuid), data=request.DELETE)
    else:
        req = requests.get(SERVER_URL + '/api/task/{}/'.format(uuid), data=request.GET)
    return JsonResponse(data=req.json())

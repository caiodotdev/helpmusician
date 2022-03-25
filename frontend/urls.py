from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    re_path('lista/', views.IndexView.as_view(), name='lista'),
    re_path('mixer/.*/', views.MixerView.as_view(), name='mixer'),
    path('api/search/', views.YouTubeSearchView.as_view()),
    path('api/source-file/all/', views.SourceFileListView.as_view()),
    path(
        'api/source-file/file/',
        views.SourceFileView.as_view({
            'post': 'create',
            'delete': 'perform_destroy'
        })),
    path('api/source-file/youtube/', views.YTLinkInfoView.as_view()),
    path('api/source-track/', views.SourceTrackListView.as_view()),
    path('api/source-track/<uuid:id>/',
         views.SourceTrackRetrieveUpdateDestroyView.as_view()),
    path('api/source-track/file/', views.FileSourceTrackView.as_view()),
    path('api/source-track/youtube/', views.YTSourceTrackView.as_view()),
    path('api/mix/static/', views.StaticMixCreateView.as_view()),
    path('api/mix/static/<uuid:id>/',
         views.StaticMixRetrieveDestroyView.as_view()),
    path('api/mix/dynamic/', views.DynamicMixCreateView.as_view()),
    path('api/mix/dynamic/<uuid:id>/',
         views.DynamicMixRetrieveDestroyView.as_view()),
    # path('api/task/', views.task_create),
    # path('api/task/<uuid:id>/', views.task_crud)
]

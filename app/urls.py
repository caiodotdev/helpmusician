from django.urls import path, include
from . import views

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.logout_user,
        name='logout'
    ),
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),
    # music
    path(
        '',
        views.SearchTemplate.as_view(),
        name='index'
    ),
    path(
        'results/',
        views.ResultsView.as_view(),
        name='results'
    ),
    path(
        'confirm-artist',
        views.ConfirmMusic.as_view(),
        name='confirm_artist'
    ),
    path(
        'video/',
        views.VideoView.as_view(),
        name='video'
    )

]

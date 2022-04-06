from django.urls import path

from .views.auth import LoginView, LogoutUser, RegisterView
from .views.musician_views import ListTracks, ResultsView, ConfirmMusic, DrumKit, PadContinuous, CustomMixer, \
    DeleteDynamic, PlayerView, SelectedView, SelectedOut, ConfirmAddMusic

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutUser.as_view(),
        name='logout'
    ),
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),
    # music
    path(
        'app/',
        ListTracks.as_view(),
        name='index'
    ),
    path(
        'results/',
        ResultsView.as_view(),
        name='results'
    ),
    path(
        'confirm-artist/',
        ConfirmMusic.as_view(),
        name='confirm_artist'
    ),
    path(
        'drumkit/',
        DrumKit.as_view(),
        name='drumkit'
    ),
    path(
        'worship-pads/',
        PadContinuous.as_view(),
        name='worship_pads'
    ),
    path(
        'custom-mix/<uuid:id>/',
        CustomMixer.as_view(),
        name='custom_mix'
    ),
    path(
        'custom-mix/<uuid:id>/delete/',
        DeleteDynamic.as_view(),
        name='delete_mix'
    ),
    path(
        'track/<uuid:id>/',
        PlayerView.as_view(),
        name='player_view'
    ),
    path(
        'selected/',
        SelectedView.as_view(),
        name='selected'
    ),
    path(
        'music-selected/',
        SelectedOut.as_view(),
        name='selected_out'
    ),
    path(
        'confirm-add-music/',
        ConfirmAddMusic.as_view(),
        name='confirm_add_music'
    )

]

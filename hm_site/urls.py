from django.urls import path

from .views import IndexSite, TermosView, PrivacyView, CookiesView

urlpatterns = [
    path(
        '',
        IndexSite.as_view(),
        name='index_site'
    ),
    path(
        'terms/',
        TermosView.as_view(),
        name='terms'
    ),
    path(
        'privacy/',
        PrivacyView.as_view(),
        name='privacy'
    ),
    path(
        'cookie-policies/',
        CookiesView.as_view(),
        name='cookies'
    ),
]

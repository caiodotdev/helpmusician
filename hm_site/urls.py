from django.urls import path

from .views import IndexSite

urlpatterns = [
    path(
        '',
        IndexSite.as_view(),
        name='index_site'
    ),
]

# Create your views here.
from django.views.generic import TemplateView


class IndexSite(TemplateView):
    template_name = 'index_site.html'


class TermosView(TemplateView):
    template_name = 'termos.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'


class CookiesView(TemplateView):
    template_name = 'cookies.html'

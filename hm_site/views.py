from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class IndexSite(TemplateView):
    template_name = 'index_site.html'

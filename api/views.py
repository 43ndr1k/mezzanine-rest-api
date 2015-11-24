from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import list_route

from rest_framework.pagination import PageNumberPagination
import django_filters



class BlogViewSet(viewsets.ViewSet):

    def list(self, request):
        return HttpResponse([{"info":"ficken"},])

    @list_route()
    def wordcloud(self, request):
        return HttpResponse([{"text":"foo", "size":25}, {"text":"foobar", "size":17}, {"text":"bar", "size":12}, {"text":"shownotes", "size":5}])


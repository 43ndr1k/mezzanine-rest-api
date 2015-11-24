from __future__ import unicode_literals
from .views import BlogViewSet
from django.conf.urls import url, include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'blog', BlogViewSet, base_name='blogrest')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
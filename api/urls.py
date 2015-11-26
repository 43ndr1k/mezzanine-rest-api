from __future__ import unicode_literals
from django.conf.urls import url, include

from rest_framework import routers
from .views import BlogViewSet, PageViewSet, PostViewSet, UserViewSet, CategoryViewSet, SiteViewSet, BlogPostViewSet

router = routers.DefaultRouter()
router.register(r'blog', BlogViewSet, base_name='getpost')
router.register(r'pages', PageViewSet)
router.register(r'posts', PostViewSet, 'posts')
router.register(r'post', BlogPostViewSet, 'post')
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'site', SiteViewSet, SiteViewSet.as_view({'get': 'retrieve'}))

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
















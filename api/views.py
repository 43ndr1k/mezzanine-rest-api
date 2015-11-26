from django.contrib.admin import filters
from django.http import HttpResponse
from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import PageNumberPagination
import django_filters

from .serializers import UserSerializer, PostsSerializer, CategorySerializer, PostSerializer
from .serializers import PageSerializer, SiteSerializer
from .permissions import IsAdminOrReadOnly
from .mixins import PutUpdateModelMixin

from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost as Post, BlogCategory, BlogPost
from mezzanine.pages.models import Page
from django.contrib.sites.models import Site
from django.views.decorators.cache import never_cache

class BlogViewSet(viewsets.ViewSet):

    def list(self, request):
        return HttpResponse([{"info":"ficken"},])

    @list_route()
    def wordcloud(self, request):
        return HttpResponse([{"text":"foo", "size":25}, {"text":"foobar", "size":17}, {"text":"bar", "size":12}, {"text":"shownotes", "size":5}])

    @list_route()
    @never_cache
    def bloglist(self, request):
        post = Post.objects.published().all().order_by("-publish_date")

        return HttpResponse(post)

class CustomPagination(PageNumberPagination):
    """
    Default pagination class.
    Let large result sets be split into individual pages of data.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostPagination(CustomPagination):
    """
    Pagination for Blog Posts
    """
    page_size = 5


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    For listing or retrieving pages.
    ---
    list:
        parameters:
            - name: page
              type: integer
              description: Page number
              paramType: query
    """
    queryset = Page.objects.published()
    serializer_class = PageSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if not user.is_authenticated():
            queryset = queryset.filter(login_required=False)

        return (queryset)

class PostFilter(django_filters.FilterSet):
    """
    A class for filtering blog posts.
    """
    category_id = django_filters.NumberFilter(name="categories__id")
    category_name = django_filters.CharFilter(name="categories__title", lookup_type='contains')
    tag = django_filters.CharFilter(name='keywords_string', lookup_type='contains')
    author_id = django_filters.NumberFilter(name="user__id")
    author_name = django_filters.CharFilter(name="user__username", lookup_type='istartswith')
    date_min = django_filters.DateFilter(name='publish_date', lookup_type='gte')
    date_max = django_filters.DateFilter(name='publish_date', lookup_type='lte')

    class Meta:
        model = Post
        fields = ['category_id', 'category_name', 'tag', 'author_id', 'author_name', 'date_min', 'date_max']


class BlogPostView(viewsets.ReadOnlyModelViewSet,
                   viewsets.GenericViewSet):
    pass

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    For listing or retrieving blog posts.
    ---
    list:
        parameters:
            - name: category_id
              type: integer
              description: Filter posts by category ID
              paramType: query
            - name: category_name
              type: string
              description: Filter posts by category name
              paramType: query
            - name: tag
              type: string
              description: Filter posts by tag name
              paramType: query
            - name: author_id
              type: integer
              description: Filter posts by author ID
              paramType: query
            - name: author_name
              type: string
              description: Filter posts by author's username
              paramType: query
            - name: search
              type: string
              description: Search for blog posts that match the query
              paramType: query
            - name: page
              type: integer
              description: Page number
              paramType: query
    """

    queryset = Post.objects.published().all().order_by("-publish_date")
    filter_class = PostFilter
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('title', 'content',)
    serializer_class = PostsSerializer
    pagination_class = PostPagination



class BlogPostViewSet(viewsets.GenericViewSet):
    """
    For listing, retrieving, creating or updating Blog Post.
    """

    # prüfen der daten

    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]


    def create(self, request, *args, **kwargs):

        post = BlogPost(user_id=request.data['user'],
                        title=request.data['title'],
                        content='<p>'+request.data['content']+'</p>',
                        status=2,
                        featured_image=''
        )

        for key,value in request.data.items():
            if key == 'status':
                post.status = value
            if key == 'gen_description':
                post.gen_description = value
            if key == 'in_sitemap':
                post.in_sitemap = value
            if key == 'slug':
                post.slug = value
            if key == 'featured_image':
                post.featured_image = value
            if key == 'allow_comments':
                post.allow_comments = value
            if key == 'gen_description':
                post.gen_description = value
            if key == 'in_sitemap':
                post.in_sitemap = value

        post.save()


        return HttpResponse('<a href="'+ post.get_absolute_url() + '">' + post.title + '</a>')

    def update(self, request, pk=None):
        post = BlogPost.objects.get(id=pk)
        for key,value in request.data.items():
            if key == 'title':
                post.title = value
                post.slug = value
            if key == 'content':
                post.content = value
            if key == 'status':
                post.status = value
            if key == 'gen_description':
                post.gen_description = value
            if key == 'in_sitemap':
                post.in_sitemap = value
            if key == 'slug':
                post.slug = value
            if key == 'featured_image':
                post.featured_image = value

        post.save()

        return HttpResponse('<a href="'+ post.get_absolute_url() + '">' + post.title + '</a>')

class UserFilter(django_filters.FilterSet):
    """
    A class for filtering users.
    """
    username = django_filters.CharFilter(name="username", lookup_type='istartswith')

    class Meta:
        model = User
        fields = ['username']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    For listing or retrieving users.
    ---
    list:
        parameters:
            - name: username
              type: string
              description: Filter usernames starting with query
              paramType: query
            - name: page
              type: integer
              description: Page number
              paramType: query
    """
    queryset = User.objects.all()
    filter_class = UserFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAdminUser,)

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      PutUpdateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    For listing, retrieving, creating or updating blog categories.
    ---
    list:
        parameters:
            - name: search
              type: string
              description: Search for category names that match the query
              paramType: query
            - name: page
              type: integer
              description: Page number
              paramType: query
    """
    queryset = BlogCategory.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A viewset that provides only `list` actions.

    To use it, override the class and set the `.queryset` and `.serializer_class` attributes.
    """
    pass


class SiteViewSet(ListViewSet):
    """
    For retrieving site title, tagline and domain.
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

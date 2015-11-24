REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#    'DEFAULT_PERMISSION_CLASSES': [
#        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#    ]
}

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.23',
    'api_path': '/',
    'enabled_methods': [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    'api_key': 'foobar',
    'is_authenticated': False,
    'is_superuser': False,
    'permission_denied_handler': None,
    'resource_access_handler': None,
    #'base_path':'http://snotes20.com:8000/api-doc',
    'info': {
        'contact': 'info@it-sawade.de',
        'description': 'This is the API documenation of it-sawade.de. '
                       'More information at '
                       '<a href="https://it-sawade.des">'
                       'http://it-sawade.de</a> '
                       ,
        #'license': 'Apache 2.0',
        #'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        #'termsOfServiceUrl': 'http://helloreverb.com/terms/',
        'title': 'IT-SAWADE API',
    },
    'doc_expansion': 'none',
}

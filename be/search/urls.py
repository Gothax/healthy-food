from django.urls import path

from . import api

# config path('api/search/', include('search.urls')),
urlpatterns = [
    path('', api.search, name='search'),
]
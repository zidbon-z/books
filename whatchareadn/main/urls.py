from django.urls import path
from .views import Index, Search

app_name = 'main'

urlpatterns = [
        path('', Index.as_view(), name='index'),
        path('search/', Search.as_view(), name='search'),
]

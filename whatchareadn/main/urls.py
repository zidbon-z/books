from django.urls import path
from .views import Index, Search, Library
from . import views

app_name = 'main'

urlpatterns = [
        path('', Index.as_view(), name='index'),
        path('search/', Search.as_view(), name='search'),
        path('library/', Library.as_view(), name='library'),
        path('search/add_book/', views.add_book_view, name='add'),
        path('library/delete_book/', views.delete_book_view, name='delete'),
        path('test/', views.testpage_view, name='test'),
        path('library/shelf/', views.get_shelf, name='shelf'),
        path('library/change_shelf/', views.change_shelf, name='change-shelf'),
        path('book_detail/', views.get_book_detail, name='bookdetail'),
        path('library/delete_shelf/', views.delete_shelf, name='delete-shelf'),
        path('library/create_shelf/', views.create_shelf, name='create-shelf'),

]

from django.urls import path
from .views import Index, Search, Library, Libraryn
from . import views

app_name = 'main'

urlpatterns = [
        path('', Index.as_view(), name='index'),
        path('search/', Search.as_view(), name='search'),
        path('library/', Library.as_view(), name='library'),
        path('libraryn/', Libraryn.as_view(), name='libraryn'),
        path('library/add_book/<str:googleid>/', views.add_book_view, name='add'),
        path('search/add_another_book/', views.add_another_book_view, name='adder'),
        path('library/delete_book', views.delete_book_view, name='delete'),
        path('test/', views.testpage_view, name='test'),
        path('detail/', views.get_book_detail, name='detail'),

]

from django.urls import path
#from .views import Login
from . import views

app_name = 'users'

urlpatterns = [
        #path('login/', Login.as_view(), name='login'),
        path('login/', views.login_user, name='login'),
        path('logout/', views.logout, name='logout'),
        path('register/', views.register_user, name='register'),
]

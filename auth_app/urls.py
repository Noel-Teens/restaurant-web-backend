from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('profile/', views.profile, name='profile'),
]

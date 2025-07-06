from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('users/', views.admin_users_list, name='admin_users_list'),
    path('menu/', views.admin_add_menu_item, name='admin_add_menu_item'),
    path('menu/all/', views.admin_menu_items, name='admin_menu_items'),
    path('menu/<int:menu_id>/', views.admin_delete_menu_item, name='admin_delete_menu_item'),
    path('reviews/', views.admin_reviews_list, name='admin_reviews_list'),
    path('review/<int:review_id>/', views.admin_delete_review, name='admin_delete_review'),
]

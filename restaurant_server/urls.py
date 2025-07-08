from django.urls import path
from . import views

app_name = 'restaurant_server'

urlpatterns = [
    path('menu/', views.menu_list, name='menu_list'),
    path('reservation/', views.create_reservation, name='create_reservation'),
    path('reservations/', views.user_reservations, name='user_reservations'),
    path('order/', views.create_order, name='create_order'),
    path('orders/', views.user_orders, name='user_orders'),
    path('review/', views.create_review, name='create_review'),
    path('reviews/', views.reviews_list, name='reviews_list'),
    # Cart and checkout
    path('checkout/', views.checkout_cart, name='checkout_cart'),
    # Profile management
    path('profile/update/', views.update_user_profile, name='update_user_profile'),
]

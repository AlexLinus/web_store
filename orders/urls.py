from django.urls import path


from orders import views
urlpatterns = [
    path('add_to_cart/<str:product_slug>/', views.add_to_cart_view, name='add_to_cart_url'),
    path('remove_from_cart/<str:product_slug>/', views.remove_from_cart_view, name='remove_from_cart_url'),
    path('order/', views.get_checkout, name='get_checkout_url'),
    path('cart/', views.get_cart, name='get_cart_url'),
]

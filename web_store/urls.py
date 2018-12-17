"""web_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views
urlpatterns = [
    path('search/', views.search_form, name='search_form_url'),
    path('admin/', admin.site.urls),
    path('checkout/', include('orders.urls')),
    path('', views.home, name='home_url'),
    path('category/<str:category_slug>/', views.get_category_detail, name='get_category_detail_url'),
    path('<str:category_slug>/<str:product_slug>/', views.get_product_detail, name='get_product_detail_url'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

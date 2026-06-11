from django.contrib import admin
from django.urls import path
from pages.views import index, about


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('about/', about, name='about')
]

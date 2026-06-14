from django.urls import path
from pages.views import home, about, add_spell, edit_spell, register_view, login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',                  home,          name='home'),
    path('about/',            about,         name='about'),
    path('add-spell/',        add_spell,     name='add_spell'),
    path('edit-spell/<int:spell_id>/', edit_spell, name='edit_spell'),
    path('register/',         register_view, name='register'),
    path('login/',            login_view,    name='login'),
    path('logout/',           logout_view,   name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

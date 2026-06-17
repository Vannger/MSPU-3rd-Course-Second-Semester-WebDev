from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from pages.views import (
    home, about, spell_detail, spells_by_tag, add_spell, edit_spell,
    register_view, login_view, logout_view, feedback_view
)

urlpatterns = [
    path('',                           home,           name='home'),
    path('about/',                     about,          name='about'),
    path('spell/<int:spell_id>/',      spell_detail,   name='spell_detail'),
    path('tag/<int:tag_id>/',          spells_by_tag,  name='spells_by_tag'),
    path('add-spell/',                 add_spell,      name='add_spell'),
    path('edit-spell/<int:spell_id>/', edit_spell,     name='edit_spell'),
    path('register/',                  register_view,  name='register'),
    path('login/',                     login_view,     name='login'),
    path('logout/',                    logout_view,    name='logout'),
    path('admin/',                     admin.site.urls),
    path('feedback/',                  feedback_view,  name='feedback'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

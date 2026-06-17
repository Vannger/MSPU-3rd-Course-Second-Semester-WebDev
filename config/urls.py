from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from pages.views import (
    Home, about, SpellDetail, spells_by_tag, AddSpell, EditSpell, DeleteSpell,
    register_view, login_view, logout_view, feedback_view, add_comment
)

urlpatterns = [
    path('',                          Home.as_view(),        name='home'),
    path('about/',                    about,                  name='about'),
    path('spell/<int:pk>/',           SpellDetail.as_view(),  name='spell_detail'),
    path('tag/<int:tag_id>/',         spells_by_tag,          name='spells_by_tag'),
    path('add-spell/',                AddSpell.as_view(),     name='add_spell'),
    path('edit-spell/<int:pk>/',      EditSpell.as_view(),    name='edit_spell'),
    path('delete-spell/<int:pk>/',    DeleteSpell.as_view(),  name='delete_spell'),
    path('register/',                 register_view,          name='register'),
    path('login/',                    login_view,             name='login'),
    path('logout/',                   logout_view,            name='logout'),
    path('admin/',                    admin.site.urls),
    path('feedback/',                 feedback_view,          name='feedback'),
    path('spell/<int:pk>/comment/',   add_comment,            name='add_comment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

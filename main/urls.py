"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app.views import *
from app.wordle import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# favicon_view = RedirectView.as_view(url='/static/pinkyak.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path("home", home, name="home"),
    path("diary", diary, name="diary"),
    path("dogs", dogs, name="dogs"),
    path("dog_edit<id>", dog_edit, name="dog_edit"),
    path("booking<id>", booking, name="booking"),
    path("quotes", quotes, name="quotes"),
    path("birthdays", birthdays, name="birthdays"),
    path("events", events, name="events"),
    path("notes", notes, name="notes"),
    path("note<id>", note, name="note"),
    path("up<id>", up, name="up"),
    path("down<id>", down, name="down"),
    path("delete_note<id>", delete_note, name="delete_note"),
    path("new_category", new_category, name="new_category"),
    path("clash", clash, name="clash"),
    path("hero_inc/<id>/<hero>", hero_inc, name="hero_inc"),
    # path('pinkyak.ico', favicon_view),
    path('wordle', wordle, name='wordle'),
    path('wordle/<entry>', wordle, name='wordle'),
    path('clear', clear, name='clear')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

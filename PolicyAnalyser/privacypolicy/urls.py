from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", views.index, name='index'),
    path("home", views.home, name='home'),
    path("download", views.download_txt, name='download'),
    path("summary", views.render_pdf_view, name='summary'),

]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('locate_get.html', views.locate_get, name='locate_get'),
    path('holiday.html', views.holiday, name='holiday'),
]
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/',views.index),
    path('load-data/',views.loadData),

]

rom django.urls import path

from . import views

app_name = 'unifiedfugitivedatabase'
urlpatterns = [
    path('', views.search, name='search'),
    path('database/', views.database, name='database'),
    # path('<int>/records/', views.record, name='records'),
    path('analytics/', views.analytics, name='analytics'),
    path('map/', views.map, name='map'),
    path('about/', views.about, name='about'),
]

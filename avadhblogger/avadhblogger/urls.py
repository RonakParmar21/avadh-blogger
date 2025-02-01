from django.contrib import admin #type: ignore
from django.urls import path #type: ignore
from avadhblog import views

urlpatterns = [
    path('', views.Index, name='home'),
    path('/about/', views.About, name='about'),
    path('/article/', views.Article, name='article'),
    path('/category/', views.Category, name='category'),
]

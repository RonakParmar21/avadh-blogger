from django.contrib import admin #type: ignore
from django.urls import path # type: ignore
from django.conf import settings  #type: ignore
from avadhblog import views
import os
from django.conf.urls.static import static #type: ignore

urlpatterns = [
    path('', views.Index, name='home'),
    path('about/', views.About, name='about'),
    path('article/', views.Article, name='article'),
    path('category/', views.Category, name='category'),
    path('login/', views.Login, name='login'),
    path('registration/', views.Registration, name='registration'),
    path('avadhblog/', views.AdminDashborad, name='admin-dashboard'), 
    path('avadhblog/login/', views.AdminLogin, name='adminlogin'),
    path('avadhblog/addBlog/', views.AddBlog, name='addblog'),
    path('avadhblog/viewBlog/', views.ViewBlog, name='viewblog'),
    path('avadhblog/delete-blog/<int:id>/', views.DeleteBlog, name='delete_blog'),
    path('avadhblog/update-blog/<int:id>/', views.UpdateBlog, name='update_blog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
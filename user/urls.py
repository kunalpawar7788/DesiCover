from django.contrib import admin
from django.urls import path
from user import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('signOut/', views.signOut, name="signout"),
    # url(r'^oauth/', include('social_django.urls', namespace='social')),
]

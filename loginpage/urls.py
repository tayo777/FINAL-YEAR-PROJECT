from django.contrib import admin
from django.urls import path, include
from loginpage import views


urlpatterns = [
    path('home', views.home, name="home"),
    path('welcome', views.welcome, name="welcome"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('signout_user', views.signout_user, name="signout_user"),
    path('namesearch', views.namesearch, name='namesearch'),
    path('descsearch', views.descsearch, name='descsearch'),
    path('search_results', views.search_results, name='search_results'),


]
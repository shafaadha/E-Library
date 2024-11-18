from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='profile_edit'),
    path('logout/', views.logout, name='logout'),
    path('', views.login, name='login'),
]


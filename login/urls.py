from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login),
    path('login/', views.login),
    path('signin/', views.signin),
    path('dropbox_upload/', views.dropbox_upload, name='dropbox_upload'),
    path('user_table/', views.user_table, name='user_table'),
    path('update_user/<str:email>/', views.update_user, name='update_user'),
    path('delete_user/<str:email>/', views.delete_user, name='delete_user'),
]
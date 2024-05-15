from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_index, name="login_index"),
    path('auth/', views.login_auth, name="login_auth"),
    path('exit/', views.login_logout, name="login_logout")
]

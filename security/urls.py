from django.urls import path
from . import views

urlpatterns = [
    path("", views.security_index, name="security_index"),
    path("security/toolsimage", views.security_create_image_tool, name="security_create_image_tool"),

    
]
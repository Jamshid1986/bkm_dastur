from django.urls import path
from . import views

urlpatterns = [
    path("", views.reception_index, name="reception_index"),
    path("detail/", views.reception_detail, name="reception_detail"),
    path("create/", views.reception_create_session, name="reception_create_session"),
    path("delete/", views.reception_delete_session, name="reception_delete_session"),
    path("guest/", views.reception_guest, name="reception_guest"),
    path("guest/create", views.reception_create_guest, name="reception_create_guest")
]
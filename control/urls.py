from django.urls import path
from . import views


urlpatterns = [
    path('', views.control_index, name="control_index"),

    # Country
    path('country/', views.control_country, name="control_country"),
        path('country/create/', views.control_country_create, name="control_country_create"),
        path('country/delete/', views.control_country_delete, name="control_country_delete"),
        path('country/edit/', views.control_country_edit, name="control_country_edit"),
    # Company
    path('company/', views.control_company, name="control_company"),
        path('company/create/', views.control_company_create, name="control_company_create"),
        path('company/delete/', views.control_company_delete, name="control_company_delete"),
        path('company/edit/', views.control_company_edit, name="control_company_edit"),
    # Personal
    path('personal/', views.control_personal, name="control_personal"),
        path('personal/create/', views.control_personal_create, name="control_personal_create"),
        path('personal/delete/', views.control_personal_delete, name="control_personal_delete"),
        path('personal/edit/', views.control_personal_edit, name="control_personal_edit"),
        #Document
        path('document/create/', views.control_document_create, name="control_document_create"),
        path('document/delete/<int:id>', views.control_document_delete, name="control_document_delete"),
    
    # User
    path('user/', views.control_user, name="control_user"),
        path('user/create/', views.control_user_create, name="control_user_create"),
        path('user/delete/', views.control_user_delete, name="control_user_delete"),
        path('user/edit/', views.control_user_edit, name="control_user_edit"),
        path('user/edit/pwd/', views.control_user_edit_pwd, name="control_user_edit_pwd"),
    
    path('search/', views.control_search, name='control_search'),
        path('search/go/', views.control_search_go, name="control_search_go"),
        path('search/create/excel/', views.control_to_excel, name="control_to_excel"),

    # Dastur
    path('dastur/', views.control_dastur, name="control_dastur"),
        path('dastur/create/', views.control_dastur_create, name="control_dastur_create"),
        path('dastur/<int:id>/', views.control_dastur_detail, name="control_dastur_detail"),
        path('dastur/add/', views.control_dastur_add_person, name="control_dastur_add_person"),
        path('dastur/remove/', views.control_dastur_remove_person, name="control_dastur_remove_person"),
        path('dastur/edit/', views.control_dastur_edit, name="control_dastur_edit"),
        path('dastur/delete/', views.control_dastur_delete, name="control_dastur_delete"),
    
    # Avtoulov
    path('vehicle/', views.control_vehicle, name="control_vehicle"),

]
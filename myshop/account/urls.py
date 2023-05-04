from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("main/", views.my_account, name="my_account"),
    path("login/", views.user_login, name="my_account-login"),
    path("logout/", views.user_logout, name="my_account-logout"),
    path("registration/", views.registration, name="my_account-registration"),
    path("edit_account/", views.edit_account, name="my_account-edit"),
]

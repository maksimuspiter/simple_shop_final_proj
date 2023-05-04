from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
        path("main/", views.my_account, name="my_account"),

]

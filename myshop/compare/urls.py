from django.urls import path
from . import views

app_name = "compare"
urlpatterns = [
    path("compare/", views.in_compare, name="in-compare"),
    path("list/", views.ListOfComparesListView.as_view(), name="list-of-compare"),
]

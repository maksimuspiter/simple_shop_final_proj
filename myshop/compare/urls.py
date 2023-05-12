from django.urls import path
from . import views

app_name = "compare"
urlpatterns = [
    path("add/<int:product_id>/", views.add_in_compare, name="add-in-compare")
]

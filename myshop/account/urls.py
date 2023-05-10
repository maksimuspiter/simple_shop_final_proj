from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("main/", views.AccountDetailView.as_view(), name="my_account"),
    path("main/copons/", views.AccountCopons.as_view(), name="my_copons"),
    path("main/my_favorite_products/", views.AccountFavoriteProducts.as_view(), name="my_favorite_products"),
    path("main/my_reviews/", views.AccountReviews.as_view(), name="my_reviews"),
    
    path("login/", views.user_login, name="my_account-login"),
    path("logout/", views.user_logout, name="my_account-logout"),
    path("registration/", views.registration, name="my_account-registration"),
    path("edit_account/", views.edit_account, name="my_account-edit"),
]

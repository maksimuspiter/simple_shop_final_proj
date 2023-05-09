from django.urls import path
from . import views

app_name = "support"
urlpatterns = [
    path("messages/my_messages/", views.my_messages, name="my_messages"),
    path("messages/chats/all/", views.AllChatsListView.as_view(), name="all_chats"),
    path("messages/chat/<int:pk>/", views.ChatDetailView.as_view(), name="chat"),

]

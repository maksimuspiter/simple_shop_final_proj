from django.urls import path
from . import views

app_name = "support"
urlpatterns = [
    path("messages/chats/all/", views.AllChatsListView.as_view(), name="all_chats"),
    path("messages/chat/<int:pk>/", views.ChatDetailView.as_view(), name="chat"),
    path("message/create/ajax/", views.create_message_ajax, name="create-message-ajax"),
]

from typing import Any
from django.db import models
from django.shortcuts import render, get_object_or_404
from account.models import Account
from django.contrib.auth.decorators import login_required
from .models import Message, Chat
from django.db.models import Count, Q, F
from django.views.generic import ListView, DetailView

# from shop.views import AllProductListView


@login_required
def my_messages(request):
    # account = get_object_or_404(
    #     Account.objects.select_related("user"),
    #     user=request.user,
    # )

    chats = (
        Chat.objects.filter(user=request.user)
        .select_related("status")
        .select_related("type")
        .annotate(
            unread=Count(
                "messages",
                filter=Q(messages__creator=Message.Creator.ADMIN)
                & Q(messages__viewed=False),
            )
        )
    )
    return render(
        request,
        "support/chat_window.html",
        {
            # "account": account,
            "chats": chats
        },
    )


class AllChatsListView(ListView):
    context_object_name = "chats"
    template_name = "support/all_chats.html"

    def get_queryset(self, **kwargs):
        queriset = (
            Chat.objects.filter(user=self.request.user)
            .select_related("status")
            .select_related("type")
            .annotate(
                unread=Count(
                    "messages",
                    filter=Q(messages__creator=Message.Creator.ADMIN)
                    & Q(messages__viewed=False),
                )
            )
        )
        return queriset


class ChatDetailView(DetailView):
    model = Chat
    context_object_name = "chat"
    template_name = "support/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chats = (
            Chat.objects.filter(user=self.request.user)
            .select_related("status")
            .select_related("type")
            .annotate(
                unread=Count(
                    "messages",
                    filter=Q(messages__creator=Message.Creator.ADMIN)
                    & Q(messages__viewed=False),
                )
            )
        )
        messages = self.object.messages.all()
        context["messages"] = messages
        context["chats"] = chats

        return context

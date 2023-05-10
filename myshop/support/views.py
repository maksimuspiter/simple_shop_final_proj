import json
from typing import Any
from django.db import models
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse
from .models import Message, Chat


class AllChatsListView(LoginRequiredMixin, ListView):
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


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name = "chat"
    template_name = "support/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        messages = self.object.messages.all()
        for message in messages.filter(creator=Message.Creator.ADMIN):
            message.viewed = True
            message.save()

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
        context["messages"] = messages
        context["chats"] = chats
        # context["form"] = self.request.user

        return context


@require_POST
def create_message_ajax(request):
    result = None
    error = None
    chat_id = request.POST.get("chat_id", None)
    text = request.POST.get("text", None)
    print(request.POST)

    if chat_id and text:
        try:
            result = True
            chat = get_object_or_404(Chat, id=chat_id)
            Message.objects.create(chat=chat, text=text, creator=Message.Creator.USER)

        except Chat.DoesNotExist:
            error = "This chat doesn not exite"

    else:
        error = "Invalid data"

    return HttpResponse(
        json.dumps({"result": result, "text": text, "error": error}),
        content_type="application/json",
    )

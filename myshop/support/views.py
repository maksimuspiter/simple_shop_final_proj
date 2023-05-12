import json
from typing import Any, Optional
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
    queryset = Chat.objects.all().select_related("user")
    context_object_name = "chat"
    template_name = "support/chat.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        messages = self.object.messages.all()
        old_messages = messages
        unread_messages = None
        unread_message_quantity = len(
            messages.filter(viewed=False, creator=Message.Creator.ADMIN)
        )
        if unread_message_quantity:
            old_messages = messages[: len(messages) - unread_message_quantity]
            unread_messages = messages[len(messages) - unread_message_quantity :]

        chats = (
            Chat.objects.filter(user=self.request.user)
            .select_related("type")
            .prefetch_related("messages")
            .annotate(
                unread=Count(
                    "messages",
                    filter=Q(messages__creator=Message.Creator.ADMIN)
                    & Q(messages__viewed=False),
                )
            )
        )
        context["old_messages"] = old_messages
        context["unread_messages"] = unread_messages
        context["chats"] = chats
        context["chat_id"] = self.object.id

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


@require_POST
def read_message(request):
    result = None
    error = None
    chat_id = request.POST.get("chat_id", None)

    if chat_id:
        try:
            result = True
            chat = get_object_or_404(Chat, id=chat_id)
            for message in chat.messages.filter(creator="A", viewed=False):
                message.viewed = True
                message.save()
        except Message.DoesNotExist:
            error = "Message does not exist"

    return HttpResponse(
        json.dumps({"result": result, "error": error}),
        content_type="application/json",
    )

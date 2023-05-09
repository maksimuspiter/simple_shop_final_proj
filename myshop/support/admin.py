from django.contrib import admin
from .models import Status, Type, Chat, Message
from django.contrib.admin import  widgets
from django.db import models
from django.forms import Textarea, TextInput 


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_display_links = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    list_display_links = ["name"]
    prepopulated_fields = {"slug": ("name",)}


class MessagesInline(admin.TabularInline):
    model = Message
    raw_id_fields = ["chat"]
    extra = 2
    formfield_overrides = {
    models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})},
}  


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "type",
        "status",
    ]
    list_filter = ["type", "status"]
    list_display_links = ["id", "user"]
    inlines = [MessagesInline]

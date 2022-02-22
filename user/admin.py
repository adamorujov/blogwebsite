from django.contrib import admin
from user.models import CustomUser, Subscriber, Newsletter

def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'conf_num', 'confirmed']
    list_filter = ['confirmed']
    search_fields = ['email']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ["subject", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["email"]
    actions = [send_newsletter]

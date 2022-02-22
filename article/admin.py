from django.contrib import admin
from .models import Article, Category, Message, Tag, Comment, ContactInfo, Message

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "created_date"]
    list_display_links = ["title"]
    list_filter = ["created_date"]
    search_fields = ["title", "author__username"]
    search_help_text = "Search by author username"
    empty_value_display = '-empty-'
    fieldsets = (
        ("Important", {
            "fields": (
                'author', 'title', 'slug' ,'main_article_image', 'article_image', 'article_blur_image', 'categories', 'tags', 'content'
            ),
            "classes": (
                'wide',
            ),
            "description": "This is important part of Article Model."
        }),
    )
    

    class Meta:
        model = Article

admin.site.register(Category)
admin.site.register(Tag)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'email', 'sent_date']
    list_filter = ['sent_date']
    search_fields = ['subject', 'message', 'name', 'email']

    class Meta:
        model = Message


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'article', 'name', 'pub_date']
    list_filter = ['pub_date']
    search_fields = ['comment','name', 'article__title']

    class Meta:
        model = Comment

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact Info", {
            'fields': ('phonenumber', 'emailadress', 'streetadress', 'map_address_link'),
            'description': "Warning. You cannot add more than on contact info."
        },
        ),
    )
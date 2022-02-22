from django.urls import path
from article import views
from article.models import Article

app_name = "article"
urlpatterns = [
    path('detail/<slug:slug>/', views.PostDetailView.as_view(), name="detail"),
    path('blog-entries/', views.BlogEntriesView.as_view(), name="blog-entries"),
    path('category/<int:id>/', views.CategoryBlogEntriesView.as_view(), name="categoryblog"),
    path('tag/<int:id>/', views.TagBlogEntriesView.as_view(), name="tagblog"),
]
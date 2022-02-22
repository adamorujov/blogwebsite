from django.db import models
from django.contrib import admin
from ckeditor.fields import RichTextField
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

CustomUser = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    author = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=250)
    main_article_image = models.FileField(blank=True,null=True)
    article_image = models.FileField(blank=True,null=True)
    article_blur_image = models.FileField(blank=True,null=True)
    categories = models.ManyToManyField(Category, related_name="category_articles")
    tags = models.ManyToManyField(Tag, related_name="tag_articles")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    read_times = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, default="")

    @property
    def full_name(self):
        return self.author.first_name + ' ' + self.author.last_name

    def _generate_unique_slug(self):
        unique_slug = slugify(self.title)
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(unique_slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse("article:detail", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + " | " + self.author.username


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="child_comments", blank=True, null=True)
    name = models.CharField(max_length=70, default="")
    email = models.EmailField(max_length=100, default="")
    subject = models.CharField(max_length=200, default="")
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20] + "..."

class Message(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    number = models.CharField(max_length=20, default="")
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class ContactInfo(models.Model):
    phonenumber = models.CharField(max_length=20)
    emailadress = models.CharField(max_length=50)
    streetadress = models.TextField()
    map_address_link = models.URLField(max_length=500, default="")

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"

    def save(self, *args, **kwargs):
        if ContactInfo.objects.exists() and self != ContactInfo.objects.first():
            pass
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return "Contact Info"

    

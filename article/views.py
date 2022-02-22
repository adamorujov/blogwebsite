from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from article.models import Article, Category, Tag, Comment, Message, ContactInfo
from user.models import Subscriber
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

class HomeView(View):
    template_name = 'index.html'
    most_read_articles = Article.objects.order_by("-read_times")[:6]
    recent_articles = Article.objects.order_by("-id")[:3]
    recent_fixed_articles = Article.objects.order_by("-id")[:3]
    categories = Category.objects.order_by("name")
    tags = Tag.objects.order_by("name")

    context = {
        'most_read_articles': most_read_articles,
        'recent_articles': recent_articles,
        'recent_fixed_articles': recent_fixed_articles,
        'categories': categories,
        'tags': tags,
        }

    def get(self, request):
        query = request.GET.get("q")
        if query:
            if request.is_ajax():
                self.searching_articles = Article.objects.filter(title__icontains=query).values()[:5]
                data = list(self.searching_articles)
                return JsonResponse(data, safe=False)

            else:
                self.recent_articles = Article.objects.order_by("-id").filter(
                    Q(title__icontains=query) | 
                    Q(content__icontains=query) | 
                    Q(author__username__icontains=query) |
                    Q(categories__name__icontains=query) |
                    Q(tags__name__icontains=query)
                )
                self.context["recent_articles"] = self.recent_articles
            self.context["query"] = query

        return render(request, self.template_name, self.context)

    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get("email")
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You have already sent your email.")
            return redirect("index")
        else:
            sub = Subscriber(email=email, conf_num=random_digits())
            sub.save()
            new_message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='Thank you for signing up for my email newsletter! \
                   Please complete the process by \
                   <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                   confirm your registration</a>.'.format(request.build_absolute_uri(''),sub.email, sub.conf_num),
                   )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            print(sg.send(new_message))
            messages.success(request, "Please, go to your email and confirm your subscription.")
            return redirect("index")

def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        messages.success(request, "Your subscription confirmed successfully.")
        return redirect("index")
    else:
        messages.info(request, "Your confirmation denied.")
        return redirect("index")

def deleteConfirmation(request):
    sub = Subscriber.objects.get(email=request.GET.get('email'))
    if sub.conf_num == request.GET.get('conf_num'):
        sub.delete()
        messages.success(request, "You deleted your subscription, successfully.")
        return redirect("index")
    else:
        messages.info(request, "You could not delete your subscription.")
        return redirect("index")


def about(request):
    return render(request, "about.html")

class BlogEntriesView(View):
    template_name = 'blog.html'
    articles = Article.objects.order_by("-id")
    recent_fixed_articles = Article.objects.order_by("-id")[:3]
    categories = Category.objects.order_by("name")
    tags = Tag.objects.order_by("name")

    context = {
        'articles': articles,
        'recent_fixed_articles': recent_fixed_articles,
        'categories': categories,
        'tags': tags,
        }

    def get(self, request):
        query = request.GET.get("q")
        if query:
            if request.is_ajax():
                self.searching_articles = Article.objects.filter(title__icontains=query).values()[:5]
                data = list(self.searching_articles)
                return JsonResponse(data, safe=False)

            else: 
                self.articles = self.articles.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(categories__name__icontains=query) |
                    Q(tags__name__icontains=query)
                )
                self.context["articles"] = self.articles
            self.context["query"] = query


        paginator = Paginator(self.articles, 2)
        page_number = request.GET.get("page")
        self.page_obj = paginator.get_page(page_number)

        self.context["page_obj"] = self.page_obj

        return render(request, self.template_name, self.context)

    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get("email")
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You have already sent your email.")
            return redirect("index")
        else:
            sub = Subscriber(email=email, conf_num=random_digits())
            sub.save()
            new_message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='Thank you for signing up for my email newsletter! \
                   Please complete the process by \
                   <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                   confirm your registration</a>.'.format(request.build_absolute_uri(''),sub.email, sub.conf_num),
                   )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            print(sg.send(new_message))
            messages.success(request, "Please, go to your email and confirm your subscription.")
            return redirect("index")


class CategoryBlogEntriesView(View):
    template_name = 'categoryblog.html'
    recent_fixed_articles = Article.objects.order_by("-id")[:3]
    categories = Category.objects.order_by("name")
    tags = Tag.objects.order_by("name")

    context = {
        'recent_fixed_articles': recent_fixed_articles,
        'categories': categories,
        'tags': tags,
        }

    def get(self, request, id):
        self.category = Category.objects.get(id=id)
        self.articles = self.category.category_articles.order_by("-id")
        self.context["category"] = self.category
        self.context["articles"] = self.articles
        query = request.GET.get("q")
        if query:
            if request.is_ajax():
                self.searching_articles = Article.objects.filter(title__icontains=query).values()[:5]
                data = list(self.searching_articles)
                return JsonResponse(data, safe=False)

            else: 
                self.articles = self.articles.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(categories__name__icontains=query) |
                    Q(tags__name__icontains=query)
                )
                self.context["articles"] = self.articles
            self.context["query"] = query


        paginator = Paginator(self.articles, 2)
        page_number = request.GET.get("page")
        self.page_obj = paginator.get_page(page_number)

        self.context["page_obj"] = self.page_obj

        return render(request, self.template_name, self.context)

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        email = request.POST.get("email")
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You have already sent your email.")
            return redirect("index")
        else:
            sub = Subscriber(email=email, conf_num=random_digits())
            sub.save()
            new_message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='Thank you for signing up for my email newsletter! \
                   Please complete the process by \
                   <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                   confirm your registration</a>.'.format(request.build_absolute_uri(''),sub.email, sub.conf_num),
                   )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            print(sg.send(new_message))
            messages.success(request, "Please, go to your email and confirm your subscription.")
            return redirect("index")


class TagBlogEntriesView(View):
    template_name = 'tagblog.html'
    recent_fixed_articles = Article.objects.order_by("-id")[:3]
    categories = Category.objects.order_by("name")
    tags = Tag.objects.order_by("name")

    context = {
        'recent_fixed_articles': recent_fixed_articles,
        'categories': categories,
        'tags': tags,
        }

    def get(self, request, id):
        self.tag = Tag.objects.get(id=id)
        self.articles = self.tag.tag_articles.order_by("-id")
        self.context["tag"] = self.tag
        self.context["articles"] = self.articles
        query = request.GET.get("q")
        if query:
            if request.is_ajax():
                self.searching_articles = Article.objects.filter(title__icontains=query).values()[:5]
                data = list(self.searching_articles)
                return JsonResponse(data, safe=False)

            else: 
                self.articles = self.articles.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(author__username__icontains=query) |
                    Q(categories__name__icontains=query) |
                    Q(tags__name__icontains=query)
                )
                self.context["articles"] = self.articles
            self.context["query"] = query

        paginator = Paginator(self.articles, 2)
        page_number = request.GET.get("page")
        self.page_obj = paginator.get_page(page_number)

        self.context["page_obj"] = self.page_obj

        return render(request, self.template_name, self.context)

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        email = request.POST.get("email")
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, "You have already sent your email.")
            return redirect("index")
        else:
            sub = Subscriber(email=email, conf_num=random_digits())
            sub.save()
            new_message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='Thank you for signing up for my email newsletter! \
                   Please complete the process by \
                   <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                   confirm your registration</a>.'.format(request.build_absolute_uri(''),sub.email, sub.conf_num),
                   )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            print(sg.send(new_message))
            messages.success(request, "Please, go to your email and confirm your subscription.")
            return redirect("index")

class PostDetailView(View):
    template_name = "post-details.html"
    recent_fixed_articles = Article.objects.order_by("-id")[:3]
    categories = Category.objects.order_by("name")
    tags = Tag.objects.order_by("-id")
    
    def get(self, request, slug):
        self.article = get_object_or_404(Article, slug=slug)
        self.article.read_times += 1
        self.article.save()
        self.comments = self.article.article_comments.filter(parent=None).order_by("-id")
        self.all_comments_num = len(self.article.article_comments.all())
        query = request.GET.get("q")
        
        if query:
            if query in self.article.content:
                self.article.content = self.article.content.replace(query, "<i style='background-color:#f48840; color:white;'>%s</i>" % query)
        
        self.context = {
            'article': self.article,
            'comments': self.comments,
            'all_comments_num': self.all_comments_num,
            'recent_fixed_articles': self.recent_fixed_articles,
            'categories': self.categories,
            'tags': self.tags,
        }

        return render(request, self.template_name, self.context)

    def post(self, request, slug):
        self.article = get_object_or_404(Article, slug=slug)
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if request.POST.get("choice") == "comment":
            parent = None
        elif request.POST.get("choice") == "reply":
            id = request.POST.get("to")
            parent = Comment.objects.get(id=int(id))

        Comment.objects.create(
            article=self.article,
            parent=parent,
            name=name,
            email=email,
            subject=subject,
            comment=message,
        )

        messages.info(request, "Your comment added successfully.")
        return redirect('article:detail', slug=slug)

class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        self.contact_info = ContactInfo.objects.first()

        self.context = {
            'contact_info': self.contact_info,
        }

        return render(request, self.template_name, self.context)

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        number = request.POST.get("number")
        message = request.POST.get("message")

        Message.objects.create(
            name = name,
            email = email,
            subject = subject,
            number = number,
            message = message,
        )

        messages.info(request, "Your message sent successfully")
        return redirect('contact')


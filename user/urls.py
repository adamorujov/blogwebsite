from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path('login/', views.signUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
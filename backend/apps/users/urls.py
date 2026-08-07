from django.urls import path
from . import views
from .views import UsernameCountView

urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
]
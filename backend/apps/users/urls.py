from django.urls import path
from . import views
from .views import UsernameCountView, RegisterView, loginView, logoutView, CenterView

urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', loginView.as_view()),
    path('logout/', logoutView.as_view()),
    path('center/', CenterView.as_view()),
]
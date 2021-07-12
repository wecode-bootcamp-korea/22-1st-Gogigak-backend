from django.urls import path
from .views import SignUpView, SignInView , UserView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/me', UserView.as_view()),
]
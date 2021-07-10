from django.urls import path
from .views import SignUpView, SignInView , UserView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/mypage', UserView.as_view()),
]
from django.urls import path
from .views import SignUpView , MyPageView , SignInView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/mypage', MyPageView.as_view()),
    path('/signin', SignInView.as_view()),
]
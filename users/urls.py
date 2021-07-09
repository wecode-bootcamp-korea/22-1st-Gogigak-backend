from django.urls import path
from .views import SignUpView , MyPageView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/mypage', MyPageView.as_view()),

 
]
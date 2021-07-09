from django.urls import path

from products.views import BestItemView

urlpatterns = [
    path('/best-items', BestItemView.as_view()),
]
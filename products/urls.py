from django.urls import path

from products.views import ListingView

urlpatterns = [
    path('list', ListingView.as_view()),
]

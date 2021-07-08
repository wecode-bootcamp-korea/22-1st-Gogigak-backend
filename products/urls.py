from django.urls import path

from products.views import ListingView, ProductView

urlpatterns = [
    path('list', ListingView.as_view()),
    path('detail', ProductView.as_view()),
]

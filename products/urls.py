from django.urls import path

from products.views import ProductView, BestItemView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/best-items', BestItemView.as_view()),
]
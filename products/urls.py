from django.urls    import path

from products.views import ProductView, ListingView


urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/list', ListingView.as_view()),
]

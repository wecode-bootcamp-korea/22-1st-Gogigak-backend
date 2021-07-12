from django.urls    import path

from products.views import ProductView, ReviewView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/reviews/<int:review_id>', ReviewView.as_view()),
]
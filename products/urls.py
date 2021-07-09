from django.urls    import path

from products.views import ProductView, CategoryImageView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/category-images', CategoryImageView.as_view()),
]
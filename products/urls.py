from django.urls    import path

from products.views import ProductView, ProductsView


urlpatterns = [
    path('', ProductsView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
]

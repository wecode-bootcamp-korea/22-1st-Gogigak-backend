from django.urls    import path

from products.views import ProductView, ProductsView


urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('', ProductsView.as_view()),
]

from django.urls    import path

from products.views import ProductView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
]
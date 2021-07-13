from django.urls     import path, include

from products.views  import CategoryImageView

urlpatterns = [
    path('users', include('users.urls')),
    path('orders', include('orders.urls')),
    path('products', include('products.urls')),
    path('categories', CategoryImageView.as_view()),
]

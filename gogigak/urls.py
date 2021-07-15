from django.urls     import path, include

from products.views  import CategoryView
from users.views     import DeliveryView

urlpatterns = [
    path('users', include('users.urls')),
    path('orders', include('orders.urls')),
    path('products', include('products.urls')),
    path('categories', CategoryView.as_view()),
    path('delivery/check', DeliveryView.as_view()),
]

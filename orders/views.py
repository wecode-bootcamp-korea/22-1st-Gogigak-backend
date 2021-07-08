from django.views         import View
from django.http.response import JsonResponse

from users.models    import User
from products.models import Product
from orders.models   import CartItem

class CartView(View):
    def get(self, request):
        @login_decorator
        try:
            signed_user = request.user
            items       = CartItem.objects.filter(user=signed_user)
            cart_lists  = []
            if not items:
                return JsonResponse({'cartItems':cart_lists}, status=200)

            for item in items:

                if not Product.objects.filter(pk=item.product_options.product_id):
                    continue

                product = item.product_options.product
                cart_lists.append(
                    {
                    'thumbnail': product.thumbnail,
                    'name'     : product.name,
                    'option'   : item.product_options.option.name,
                    'price'    : product.price,
                    'grams'    : product.grams,
                    'quantity' : item.quantity
                    }
                )
            return JsonResponse({'cartItems':cart_lists}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
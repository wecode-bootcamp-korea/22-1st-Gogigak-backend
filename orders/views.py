import json

from django.views         import View
from django.http.response import JsonResponse

from users.models    import User
from orders.models   import CartItem

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            signed_user = request.user
            items       = CartItem.objects.filter(user=signed_user)
            cart_lists  = [
                    {
                    'cartItemId': item.id,
                    'thumbnail' : item.product_options.product.thumbnail,
                    'name'      : item.product_options.product.name,
                    'option'    : item.product_options.option.name,
                    'price'     : item.product_options.product.price,
                    'grams'     : item.product_options.product.grams,
                    'quantity'  : item.quantity
                    } for item in items
            ]
            return JsonResponse({'cartItems':cart_lists}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

    @login_decorator
    def patch(self, request, cart_item):
        try:
            data            = json.loads(request.body)
            signed_user     = request.user
            change_quantity = data['changeQuantity']

            if not CartItem.objects.filter(pk=cart_item, user=signed_user).exists():
                return JsonResponse({'message':'INVALID_ITEM'}, status=400)
            
            item    = CartItem.objects.get(pk=cart_item)
            product = item.product_options.product

            if (item.quantity + change_quantity) > product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)
            
            if (item.quantity + change_quantity) < 1:
                return JsonResponse({'message':'INVALID_QUANTITY'}, status=400)
            
            item.quantity += change_quantity
            item.save()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
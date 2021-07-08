from django.views         import View
from django.http.response import JsonResponse

from users.models    import User
from products.models import Product
from orders.models   import CartItem

class CartView(View):
    def get(self, request):
        try:
            user       = User.objects.get(pk=request.GET.get('user_id'))
            items      = CartItem.objects.filter(user=user)
            cart_lists = []
            if not items:
                return JsonResponse({'MESSAGE':'NO_ITEMS_IN_CART'}, status=200)
            
            for item in items:
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
            return JsonResponse({'CART_ITEMS':cart_lists}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)
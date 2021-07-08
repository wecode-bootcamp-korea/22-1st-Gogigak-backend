import json

from django.views         import View
from django.http.response import JsonResponse

from users.models    import User
from products.models import Product, Option, ProductOption
from orders.models   import CartItem

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            signed_user = request.user
            items       = CartItem.objects.filter(user=signed_user)
            cart_lists  = []
            if not items:
                return JsonResponse({'cartItems':cart_lists}, status=200)

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
            return JsonResponse({'cartItems':cart_lists}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
    
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            signed_user=request.user
            product = Product.objects.get(pk=data['productId'])
            option = Option.objects.get(pk=data['optionId'])
            quantity = data['quantity']
            if quantity > product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=200)
            product_option = ProductOption.objects.get(product=product, option=option)
            CartItem.objects.
            
        except:
            


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
    def post(self, request):
        try:
            data           = json.loads(request.body)
            signed_user    = request.user
            quantity       = data['quantity']
            
            if not Product.objects.filter(pk=data['productId']).exists():
                return JsonResponse({'message':'INVALID_PRODUCT'}, status=400)

            product = Product.objects.get(pk=data['productId'])
            
            if not Option.objects.filter(pk=data['optionId']).exists():
                return JsonResponse({'message':'INVALID_OPTION'}, status=400)

            option = Option.objects.get(pk=data['optionId'])
            
            if not ProductOption.objects.filter(product=product, option=option).exists():
                return JsonResponse({'message':"INVALID_PRODUCTS_OPTION"}, status=400)
            
            product_option = ProductOption.objects.get(product=product, option=option)

            if quantity < 1:
                return JsonResponse({'message':'INVALID_QUANTITY'}, status=400)

            if quantity > product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)

            if CartItem.objects.filter(user = signed_user, product_options = product_option):
                cart_item = CartItem.objects.get(user = signed_user, product_options = product_option)

                if (cart_item.quantity + quantity) > product.stock:
                    return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)
                
                cart_item.quantity += quantity
                cart_item.save()
                return JsonResponse({'message':'SUCCESS'}, status=201)
            
            CartItem.objects.create(
                user            = signed_user,
                product_options = product_option,
                quantity        = quantity
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

import json

from django.views         import View
from django.http.response import JsonResponse

from utils           import login_decorator
from users.models    import User
from products.models import Product, Option, ProductOption
from orders.models   import CartItem, Order

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            signed_user = User.objects.get(pk=1)
            items       = CartItem.objects.filter(user=signed_user).select_related(
                'product_options',
                'product_options__product'
                )
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
            is_first = not Order.objects.filter(user=signed_user).exists()
            return JsonResponse({'isFirst': is_first,'cartItems':cart_lists}, status=200)
        
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
            product_id     = data['productId']
            option_id      = data['optionId']
            
            if quantity < 1:
                return JsonResponse({'message':'INVALID_QUANTITY'}, status=400)

            if not Product.objects.filter(pk=data['productId']).exists():
                return JsonResponse({'message':'INVALID_PRODUCT'}, status=400)

            if not Option.objects.filter(pk=data['optionId']).exists():
                return JsonResponse({'message':'INVALID_OPTION'}, status=400)

            if not ProductOption.objects.filter(product_id=product_id, option_id=option_id).exists():
                return JsonResponse({'message':"INVALID_PRODUCTS_OPTION"}, status=400)
            
            product_option = ProductOption.objects.get(product=product_id, option=option_id)

            if quantity > product_option.product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)

            cart_item, is_created = CartItem.objects.get_or_create(
                user            = signed_user,
                product_options = product_option,
                defaults        = {'quantity': quantity}
            )
            
            if not is_created:
                cart_item.quantity += quantity

            if cart_item.quantity > product_option.product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)
                
            cart_item.save()
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, cart_item):
        try:
            signed_user = request.user

            if cart_item == 0:
                items = CartItem.objects.filter(user=signed_user)
                items.delete()
                return JsonResponse({'message':'DELETE_SUCCESS'}, status=204)

            if not CartItem.objects.filter(pk=cart_item, user=signed_user).exists():
                return JsonResponse({'message':'NOT_FOUND'}, status=404)

            CartItem.objects.get(pk=cart_item, user=signed_user).delete()
            return JsonResponse({'message':'DELETE_SUCCESS'}, status=204)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=200)
            
    @login_decorator
    def patch(self, request, cart_item):
        try:
            data            = json.loads(request.body)
            signed_user     = request.user
            change_quantity = data['changeQuantity']

            if not CartItem.objects.filter(pk=cart_item, user=signed_user).exists():
                return JsonResponse({'message':'NOT_FOUND'}, status=404)

            item           = CartItem.objects.get(pk=cart_item)
            product        = item.product_options.product
            total_quantity = item.quantity + change_quantity

            if total_quantity < 1:
                total_quantity = 1

            if total_quantity > product.stock:
                return JsonResponse({'message':'OUT_OF_STOCK'}, status=400)

            item.quantity = total_quantity
            item.save()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
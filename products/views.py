import json

from django.views         import View
from django.http.response import JsonResponse

from users.models         import User
from products.models      import Category, Product, Review

class CategoryImageView(View):
    def get(self, request):
        results = [{
                'id'   : category.id,
                'name' : category.name,
                'image': category.image
            } for category in Category.objects.all()]
        
        return JsonResponse({'results': results}, status=200)

class ProductView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message': 'PRODUCT_NOT_FOUND'}, status=400)

        product        = Product.objects.get(id=product_id)

        price_per_100g = round((int(product.price) / int(product.grams) * 100))
        options        = product.options.all()
        images         = product.image_set.all()
    
        results = {
            'name'         : product.name,
            'butcheredDate': product.butchered_date,
            'price'        : int(product.price),
            'grams'        : int(product.grams),
            'pricePer100g' : price_per_100g,
            'isOrganic'    : product.is_organic,
            'thumbnail'    : product.thumbnail,
            'options'      : [option.name for option in options],
            'images'       : [{'imageUrl': image.image_url, 'sequence': image.sequence} for image in images]
        }

        return JsonResponse({'results': results}, status=200)
    
class ReviewView(View):
    # @login_decorator
    def post(self, request, product_id):
        try:
            signed_user = request.user
            data        = json.loads(request.body)
            product     = Product.objects.filter(id=product_id)

            if not product.exists():
                return JsonResponse({'message': 'PRODUCT_NOT_FOUND'}, status=404)

            Review.objects.create(
                user      = signed_user,
                product   = product,
                image_url = data['imageUrl'],
                title     = data['title'],
                content   = data['content']
            )

            product.reviews += 1
            product.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'ACCESS_DENIED'}, status=400)
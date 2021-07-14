from django.views         import View
from django.http.response import JsonResponse

from users.models         import User
from products.models      import Category, Product, Review
from utils                import login_decorator

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
    
class CategoryImageView(View):
    def get(self, request):
        results = [{
                'id'   : category.id,
                'name' : category.name,
                'image': category.image
            } for category in Category.objects.all()]
        
        return JsonResponse({'results': results}, status=200)

class ReviewView(View):
    @login_decorator
    def delete(self, request, review_id):
        try:
            signed_user = request.user
            review      = Review.objects.get(id=review_id)

            if review.user == signed_user:
                review.delete()
                review.product.reviews -= 1
                review.product.save()

                return JsonResponse({'message': "REVIEW_DELETED"}, status=204)

            else:
                return JsonResponse({'message': 'ACCESS_DENIED'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'ACCESS_DENIED'}, status=400)
from django.http.response import JsonResponse
from django.views import View

from products.models import Category, Product

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
        categories = Category.objects.all()
        results = []

        for category in categories:
            results.append(
                {
                    'name': category.name,
                    'image': category.image
                }
            )
        
        return JsonResponse({'results': results}, status=200)




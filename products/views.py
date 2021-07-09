from django.views    import View
from django.http     import JsonResponse

from products.models import Product

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
            
class BestItemView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-sales')[:6]
        results = []
       
        for product in products:
            results.append(
                {
                    'id'       : product.id,
                    'name'     : product.name, 
                    'price'    : int(product.price),
                    'grams'    : int(product.grams),
                    'thumbnail': product.thumbnail,
                    'isOrganic': product.is_organic
                }
            )
        
        return JsonResponse({'results': results}, status=200)

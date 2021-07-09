from django.views    import View
from django.http     import JsonResponse

from products.models import Product

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
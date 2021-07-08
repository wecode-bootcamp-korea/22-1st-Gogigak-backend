from django.http.response import JsonResponse
from django.views import View

from products.models import Product

class ProductView(View):
    def get(self, request):
        # product = Product.objects.get(id=product_id)
        product = Product.objects.get(id=request.GET['id'])
        print(product)
        price_per_100g = str(int(product.price) / int(product.grams) * 100)
        options = product.options.all()
        images = product.image_set.all()

        results = {
            'name': product.name,
            'butcheredDate': product.butchered_date,
            'price': product.price,
            'grams': product.grams,
            'pricePer100g': price_per_100g,
            'isOrganic': product.is_organic,
            'thumbnail': product.thumbnail,
            'options': [option.name for option in options],
            'images': [{'imageUrl': image.image_url, 'sequence': image.sequence} for image in images]
        }

        return JsonResponse({'results': results}, status=200)
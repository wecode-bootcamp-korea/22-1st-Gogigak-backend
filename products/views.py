

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Q

from products.models      import Category, Product

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

class ProductsView(View):
    def get(self, request):
        try:
            category = Category.objects.filter(name=request.GET.get('category', ''))

            q = Q()
            q.add(Q(category=category.first()), q.AND)

            products = Product.objects.filter(q)

            # if category.exists():
            #     products = Product.objects.filter(category=category[0].id)
            # else:
            #     products = Product.objects.all()

            if request.GET.get('category', '') == 'all':
                category = Category.objects.get(name='all')
                products = Product.objects.all()

            sort = {
                'sales'     : '-sales',
                'reviews'   : '-reviews',
                'price-desc': '-price',
                'price-asc' : 'price'
            }

            if request.GET.get('sort', ''):
                products = products.order_by(sort[request.GET.get('sort', '')])

            results = {
                'category_image': category[0].image if category else Category.objects.get(name='all').image,
                'items': [
                    {
                    'id'       : product.id,
                    'name'     : product.name, 
                    'price'    : int(product.price),
                    'grams'    : int(product.grams),
                    'thumbnail': product.thumbnail,
                    'isOrganic': product.is_organic,
                    'sales'    : product.sales,
                    'reviews'  : product.reviews,
                    'options'  : [{'id': option.id, 'name': option.name} for option in product.options.all()]
                    } for product in products]
                }

            return JsonResponse({'results': results}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)



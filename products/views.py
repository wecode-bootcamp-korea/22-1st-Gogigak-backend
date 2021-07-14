from django.views         import View
from django.db.models     import Q
from django.http.response import JsonResponse

from products.models      import Category, Product

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
            'options'      : [{'id': option.id, 'name': option.name} for option in options],
            'images'       : [{'imageUrl': image.image_url, 'sequence': image.sequence} for image in images]
        }

        return JsonResponse({'results': results}, status=200)

class ProductsView(View):
    def get(self, request):
        try:
            sort          = request.GET.get('sort', '')
            category_name = request.GET.get('category', None)
            category      = None
            
            q = Q()

            if Category.objects.filter(name=category_name).exists():
                category = Category.objects.get(name=category_name)
                q.add(Q(category=category), q.AND)

            sort_dict = {
                'id'        : 'id',
                'sales'     : '-sales',
                'reviews'   : '-reviews',
                'price-desc': '-price',
                'price-asc' : 'price'
            }

            results = {
                'category_image': category.image if category else None,
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
                        'options'  : [{'id': option.id, 'name': option.name} for option in product.options.all()],
                        'stock'    : product.stock
                    } for product in Product.objects.filter(q).order_by(sort_dict.get(sort, 'id'))]
                }

            return JsonResponse({'results': results}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
from django.views                import View
from django.http.response        import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from products.models             import Category, Product

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

class ListingView(View):
    def get(self, request):
        try:
            if request.GET:
                category = Category.objects.get(name=request.GET['category'])
                products = Product.objects.filter(category=category.id)
                
            if request.GET['category'] == 'all':
                category = Category.objects.get(name='all')
                products = Product.objects.all()

        except MultiValueDictKeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=400)
        
        try:
            if request.GET['sort']:
                if request.GET['sort'] == 'sales':
                    products = products.order_by('-sales')
                if request.GET['sort'] == 'reviews':
                    products = products.order_by('-reviews')
                if request.GET['sort'] == 'price-desc':
                    products = products.order_by('-price')
                if request.GET['sort'] == 'price-asc':
                    products = products.order_by('price')
        
        except MultiValueDictKeyError:
            products = products

        results = [{'category_image': category.image},[]]

        for product in products:
            results[1].append({
                'id'       : product.id,
                'name'     : product.name, 
                'price'    : int(product.price),
                'grams'    : int(product.grams),
                'thumbnail': product.thumbnail,
                'isOrganic': product.is_organic,
                'sales'    : product.sales,
                'reviews'  : product.reviews
            })

        return JsonResponse({'results': results}, status=200)

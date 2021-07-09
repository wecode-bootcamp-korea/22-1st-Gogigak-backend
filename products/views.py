import json

from django.views import View
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

# from users.models import User
from products.models import Category, Product

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

        
## 판매수 리뷰수 parameter 어떻게 들어가는지 확인(ListingView에 추가할지 새로만들지)

# # @데코레이터
# def delete(self, request):
#     user = User.objects.get(id=1)

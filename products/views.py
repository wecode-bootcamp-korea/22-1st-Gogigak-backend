import json

from django.views import View
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from products.models import Category, Product

class ListingView(View):
    def get(self, request):
        try:
            if request.GET:
                category = Category.objects.get(name=request.GET['category'])
                products = Product.objects.filter(category=category.id)
                
            if request.GET['category'] == '전체':
                products = Product.objects.all()

        except MultiValueDictKeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=400)
        
        results = []
        for product in products:
            results.append({
                'name': product.name,
                'price': int(product.price),
                'grams': int(product.grams),
                'thumbnail': product.thumbnail,
                'isOrganic': product.is_organic
            })

        return JsonResponse({'results': results}, status=200)

        
## 판매수 리뷰수 parameter 어떻게 들어가는지 확인(ListingView에 추가할지 새로만들지)

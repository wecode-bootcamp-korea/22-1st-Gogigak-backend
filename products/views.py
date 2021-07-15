import jwt, json

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Q

from users.models         import User
from products.models      import Category, Product, Review
from orders.models        import Order
from my_settings          import SECRET_KEY
from utils                import login_decorator, public_login_required

class CategoryView(View):
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

class ReviewView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            signed_user = request.user
            data        = json.loads(request.body)

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message': 'PRODUCT_NOT_FOUND'}, status=404)

            if Review.objects.filter(user=signed_user, product_id=product_id).exists():
                return JsonResponse({'message': 'REVIEW_ALREADY_EXISTS'}, status=400)

            product = Product.objects.get(id=product_id)

            Review.objects.create(
                user      = signed_user,
                product   = product,
                image_url = data['imageUrl'],
                title     = data['title'],
                content   = data['content']
            )

            product.reviews += 1
            product.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @login_decorator        
    def delete(self, request, review_id):
        signed_user = request.user

        if not Review.objects.filter(id=review_id).exists():
            return JsonResponse({'message': 'REVIEW_NOT_FOUND'}, status=404)

        review = Review.objects.get(id=review_id)

        if review.user != signed_user:
            return JsonResponse({'message': 'ACCESS_DENIED'}, status=401)

        review.delete()
        review.product.reviews -= 1
        review.product.save()

        return JsonResponse({'message': "REVIEW_DELETED"}, status=204)

    @public_login_required
    def get(self, request, product_id):
        signed_user = request.user
        product     = Product.objects.get(id=product_id)
        reviews     = Review.objects.filter(product=product)
        results = [{
            'id'            : review.id,
            'user'          : review.user.id,
            'purchaseCount' : Order.objects.filter(user=review.user).count(),
            'title'         : review.title,
            'content'       : review.content,
            'image'         : review.image_url,
            'createdAt'     : review.created_at,
            'myReview'      : True if signed_user and review.user == signed_user else False
        } for review in reviews]
        return JsonResponse({'results': results}, status=200)
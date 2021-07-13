from django.views         import View
from django.http.response import JsonResponse

from users.models         import User
from products.models      import Category, Product, Review
from orders.models        import Order
from my_settings          import SECRET_KEY

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
        results = [{
                'id'   : category.id,
                'name' : category.name,
                'image': category.image
            } for category in Category.objects.all()]
        
        return JsonResponse({'results': results}, status=200)

class ReviewView(View):
    def get(self, request, product_id):
        signed_user  = ''
        token        = request.headers.get("Authorization", None)

        if token:
            payload      = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            request.user = User.objects.get(id = payload.get('user_id', None))
            signed_user  = request.user
        
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
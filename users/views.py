import json, re, bcrypt, jwt
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY
from utils        import login_decorator

class SignUpView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            REGEX_EMAIL        = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            REGEX_PASSWORD     = re.compile(r'^[a-zA-Z0-9]{8,20}$')
            REGEX_PHONE_NUMBER = re.compile(r'^01([0|1|6|7|8|9])([0-9]{3,4})([0-9]{4})$')
            REGEX_NAME         = re.compile(r'^[가-힣]{2,5}|[a-zA-Z]{2,20}\s[a-zA-Z]{2,20}$')

            if not REGEX_EMAIL.match(data["email"]):
                return JsonResponse({"message" : "INVALID_EMAIL_FORMAT"} , status = 400) 

            if not REGEX_PASSWORD.match(data["password"]):
                return JsonResponse({"message" : "INVALID_PASSWORD_FORMAT"} , status = 400)
            
            if not REGEX_PHONE_NUMBER.match(data["phoneNumber"]):
                return JsonResponse({"message": "INVALID_PHONE_NUMBER_FORMAT"} , status = 400)
            
            if not REGEX_NAME.match(data["name"]):
                return JsonResponse({"message" : "INVALID_NAME_FORMAT"} , status = 400) 
            
            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse( {"message": "EMAIL_EXISTS"} , status = 400)

            if User.objects.filter(phone_number=data["phoneNumber"]).exists():
                return JsonResponse( {"message": "PHONE_NUMBER_EXISTS"} , status = 400)

            hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"),bcrypt.gensalt())
            
            User.objects.create(
                email        = data["email"],
                password     = hashed_password.decode("utf-8"),
                name         = data["name"],
                phone_number = data["phoneNumber"],
                address      = data["address"],
                zip_code     = data['zipCode']
                )
            return JsonResponse( {"message": "SUCCESS"} , status = 201)
        
        except KeyError:
            return JsonResponse({"message": "KeyError"} , status = 400)
        
        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"} , status = 400)

class SignInView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)

            user            = User.objects.get(email = data['email'])
            hashed_password = user.password.encode("utf-8") 
            
            if bcrypt.checkpw(data["password"].encode("utf-8"), hashed_password):
                token = jwt.encode({"user_id" : user.id}, SECRET_KEY, algorithm="HS256")
                return JsonResponse( {"message": "SUCCESS", "token": token} , status = 201)

            return JsonResponse({"message" : "INVALID_USER"}, status = 401) 
        
        except KeyError: 
            return JsonResponse({"message" : "KEY_ERROR"} , status = 400)

class UserView(View):
    # @login_decorator
    def get(self,request):
        try: 
            # user    = request.user
            user  = User.objects.get(id=1)
            orders  = user.order_set.all()
            coupons = user.coupons.all()

            results = {
                "name"       : user.name,
                "point"      : user.point,
                "coupon"     : user.coupons.all().count(),
                "userNumber" : user.id,
                "orderCount" : user.order_set.all().count(),
                "view"       : [
                    {
                        "orderNumber"  : order.id,
                        "orderSummary" : order.orderitem_set.first().product_option.product.name,
                        "totalAmount"  : order.orderitem_set.count(),
                        "totalPrice"   : order.total_price,
                        "deliveryDate" : order.delivery_date,
                    } for order in orders
                ],
                "coupons" : [
                    {   "id"          : coupon.id,
                        "name"        : coupon.name,
                        "couponValue" : coupon.value,
                    } for coupon in coupons 
                ] 
            }
            return JsonResponse( {"result": results} , status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
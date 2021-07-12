import json
import re
import bcrypt
import jwt
from json.decoder import JSONDecodeError
from utils import login_decorator

from django.views import View
from django.http  import JsonResponse
from django.db.models import Sum

from users.models import Coupon, User
from orders.models import Order
from my_settings  import SECRET_KEY

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
            
            if not REGEX_PHONE_NUMBER.match(data["phone_number"]):
                return JsonResponse({"message": "INVALID_PHONE_NUMBER_FORMAT"} , status = 400)
            
            if not REGEX_NAME.match(data["name"]):
                return JsonResponse({"message" : "INVALID_NAME_FORMAT"} , status = 400) 
            
            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse( {"message": "EMAIL_EXISTS"} , status = 400)

            if User.objects.filter(phone_number=data["phone_number"]).exists():
                return JsonResponse( {"message": "PHONE_NUMBER_EXISTS"} , status = 400)

            hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"),bcrypt.gensalt())
            
            User.objects.create(
                email        = data["email"],
                password     = hashed_password.decode("utf-8"),
                name         = data["name"],
                phone_number = data["phone_number"],
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



class MyPageDetail(View):
    @login_decorator
    def get(self,request,view):     
        user = request.user 
        orders = user.order_set.all()

        if view == 'order':
            order_results = []
            for order in orders:
                order_results.append(
                    {
                        "주문번호" : order.id,
                        "주문요약" : order.orderitem_set.first().product.name,
                        "총 개수"  : order.orderitem_set.count(),
                        "가격1"    : order.orderitem_set.first().product.price,  #하나 가격이 아닌 총 가격으로 수정필요함,,, 일단 보류
                        "가격2" : order.orderitem_set.last().product.price, # 만약 주문한 제품이 3개면 어떡해?,, 나도 몰라,,
                        "도착예정일" : order.delivery_date, 
                        }
                )
            return JsonResponse( {"results": order_results} , status = 201)

        # 2. mypage?view=coupon {"view": "coupon"} 형태로 point가 들어왔을때,
        if view=='coupon':
        
            coupons = user.coupons.all()
            result = []
            
            for coupon in coupons:
                result.append(
                    {
                    "쿠폰 이름" :coupon.name
            })
            
            return JsonResponse( {"result": result} , status = 201) #받은 쿠폰 내역


        # 3. 하드 코딩으로 처음 회원가입 적립금만 넣어주기로함 
        if view == "point":
            result = [
            {"포인트 내역" : user.point}
            ]
            return JsonResponse( {"result": result} , status = 201) #받은 쿠폰 내역
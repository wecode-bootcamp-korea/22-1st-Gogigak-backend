import json
import re
import bcrypt
import jwt
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from users.models import User, Address
from my_settings  import SECRET_KEY

from django.core.exceptions import ObjectDoesNotExist

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
            user    = request.user
            results = {
                    "name"         : user.name,
                    "point"        : user.point,
                    "coupon"       : user.coupons.all().count(),
                    "userNumber"   : user.id,
                    "orderCount"   : user.order_set.all().count(),
                    }

            return JsonResponse({"results": results} , status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class AddressView(View):
    def post(self,request):
        # try:
            data = json.loads(request.body)

            # Address.objects.get(zip_code="09999")
            address = Address.objects.get(zip_code = data["zipCode"])
            
            if int("00001") <= address.id <= int("09999"):
                return JsonResponse({'result': "배송 가능주소입니다"}, status=400)
            return JsonResponse({'result': "배송 불 가능주소입니다"}, status=400)

        # except ObjectDoesNotExist: #이 에러 처리가 필수인가,,
        #     return JsonResponse({'result': "배송불가능주소입니다222222"}, status=400)



        
        


        # address = Address.objects.get(id=1)

        # if 00001 <= address.zip_code < 000002:
        #     return True


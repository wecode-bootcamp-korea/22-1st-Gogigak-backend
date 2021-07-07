import json
import re
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError 

from users.models import User

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
                return JsonResponse({"message": "INVALID_EMAIL_FORMAT"} , status = 400)
            if not REGEX_NAME.match(data["name"]):
                return JsonResponse({"message" : "INVALID_NAME_FORMAT"} , status = 400) 
            
            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse( {"message": "EMAIL_EXISTS"} , status = 400)
            if User.objects.filter(phone_number=data["phone_number"]).exists():
                return JsonResponse( {"message": "PHONE_NUMBER_EXISTS"} , status = 400)
            
            User.objects.create(
                email        = data["email"],
                password     = data["password"],
                name         = data["name"],
                phone_number = data["phone_number"],
                )
            return JsonResponse( {"message": "SUCCESS"} , status = 201)
        
        except KeyError:
            return JsonResponse({"message": "KeyError"} , status = 400)
        except IntegrityError:
            return JsonResponse({"message": "IntegrityError"} , status = 400)
        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"} , status = 400)
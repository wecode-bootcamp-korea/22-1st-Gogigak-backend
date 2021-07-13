import jwt

from django.http  import JsonResponse

from users.models import User
from my_settings  import SECRET_KEY

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get("Authorization", None)
            payload      = jwt.decode(token, SECRET_KEY, algorithms="HS256")
            user         = User.objects.get(id = payload['user_id'])
            request.user = user
            
            return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError:     
            return JsonResponse({'message' : 'INVALID TOKEN'}, status = 400)         
    return wrapper
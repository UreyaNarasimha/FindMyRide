import jwt
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timezone

# def jwt_check(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
        
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return Response(
#                 {"detail": "invalid token"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         token = auth_header.split(" ")[1]

#         try:
#             # Decode the JWT token
#             decoded_token = AccessToken(token)

#             # Validate expiration time
#             exp_timestamp = decoded_token.get("exp")
#             if exp_timestamp:
#                 expiration_time = datetime.fromtimestamp(exp_timestamp, timezone.utc)
#                 if expiration_time < datetime.now(timezone.utc):
#                     return Response(
#                         {"detail": "Token has expired."},
#                         status=status.HTTP_401_UNAUTHORIZED,
#                     )

#             # Add the user ID to the request (or any other claim as needed)
#             # request.user_id = decoded_token.get("id")  # Match the token payload key
#             # request.username = decoded_token.get("username") 
        
#         except:
#             return Response(
#                 {"detail": "Invalid token."},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         return view_func(request, *args, **kwargs)

#     return wrapper

def jwt_check(request): #authenticating token using function
        
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(
            {"message": "invalid token",'data':{}},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.split(" ")[1]

    try:
        # Decode the JWT token
        decoded_token = AccessToken(token)

        # Validate expiration time
        exp_timestamp = decoded_token.get("exp")
        if exp_timestamp:
            expiration_time = datetime.fromtimestamp(exp_timestamp, timezone.utc)
            if expiration_time < datetime.now(timezone.utc):
                return Response(
                    {"message": "Token has expired",'data':{}},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        
        if not any(item in ['user', 'rider'] for item in decoded_token.get("type", [])):
            return Response(
                    {"message": "You are not authorized to this URL",'data':{}},
                    status=status.HTTP_401_UNAUTHORIZED,
                ) 
    
    except:
        return Response(
            {"message": "Invalid token",'data':{}},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({'message':'success','data':{}},status=status.HTTP_200_OK)

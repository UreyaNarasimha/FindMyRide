from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from six import text_type

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
                
        token['type'] = ['user']
        token['username'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        
        return token
    
def get_my_token(user_obj):

    my_token = CustomTokenObtainPairSerializer()
    refresh = my_token.get_token(user_obj)
    refresh_token = text_type(refresh)
    access_token = text_type(refresh.access_token)
    
    data = {
        'access':access_token,
        'refresh':refresh_token
    }

    return data
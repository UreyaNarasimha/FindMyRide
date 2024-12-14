from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from six import text_type

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, rider):
        token = super().get_token(rider)
                
        token['type'] = ['rider']
        token['username'] = rider.rider_name
        token['email'] = rider.email_id
        token['is_active'] = rider.is_active
        
        return token
    
def get_my_token(rider_obj):

    my_token = CustomTokenObtainPairSerializer()
    refresh = my_token.get_token(rider_obj)
    refresh_token = text_type(refresh)
    access_token = text_type(refresh.access_token)
    
    data = {
        'access':access_token,
        'refresh':refresh_token
    }

    return data
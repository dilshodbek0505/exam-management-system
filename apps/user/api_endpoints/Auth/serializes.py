from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


def authenticate(username, password):
    try:
        user = User.objects.get(username = username)
        return  user if user.check_password(password) else None
    except User.DoesNotExist:
        return None

class UserSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active=False
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 128)
    password = serializers.CharField(max_length = 128)

    def validate(self, attrs):
        username, password = attrs.get('username'), attrs.get('password')

        user = authenticate(username = username, password = password)
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        if user:
            raise serializers.ValidationError('User not active!')
        
        raise serializers.ValidationError('User not found!', 404)
        

        
        
    
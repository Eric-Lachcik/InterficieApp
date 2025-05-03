# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import CustomUser, Appointment  
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'surname', 'name', 'staff', 'email', 'role', 'entrenador', 'nutricionista']
        extra_kwargs = {'password': {'write_only': True}}

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class SecureTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'name': self.user.name,
            'surname': self.user.surname,
            'role': self.user.role,
            'is_staff': self.user.staff
        })
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Campos que viajarán en el JWT
        token['role'] = user.role
        token['is_staff'] = user.staff
        return token
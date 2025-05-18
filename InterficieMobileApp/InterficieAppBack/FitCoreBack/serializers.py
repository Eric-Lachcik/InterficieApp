# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import CustomUser, Appointment , ClientReport
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    entrenador = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='entrenador'),
        required=False,
        allow_null=True
    )
    
    nutricionista = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='nutricionista'),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'dni', 'phone', 'address', 'population', 'username',
                   'password','email', 'weight', 'muscle_mass',
                     'stature', 'fecha_registro', 'staff','role',  'entrenador', 'nutricionista']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        # Remover campos que ya tienen valor por defecto
        validated_data.pop('role', None)  # Eliminar si existe
        validated_data.pop('staff', None)  # Eliminar si existe

        entrenador_id = validated_data.pop('entrenador', None)
        nutricionista_id = validated_data.pop('nutricionista', None)

        # 1. Extraer la contraseña ANTES de crear el usuario
        raw_password = validated_data.pop('password')
        
        # 2. Crear SOLO UN usuario sin contraseña
        user = CustomUser.objects.create(
            **validated_data,
            role='cliente',  # Forzar rol de cliente
            staff=False      # Asegurar que no es staff
        )

        # Asignar relaciones
        if entrenador_id:
            user.entrenador_id = entrenador_id
        if nutricionista_id:
            user.nutricionista_id = nutricionista_id
        
        # 3. Aplicar el doble hashing personalizado
        user.set_password(raw_password)
        user.save()
    
        return user
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
            'is_staff': self.user.staff,
            'email': self.user.email,
            'phone': self.user.phone,
            'dni': self.user.dni,
            'address': self.user.address,
        })
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Campos que viajarán en el JWT
        token['role'] = user.role
        token['is_staff'] = user.staff
        return token
    
class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'surname', 'email', 'phone']


class ClientReportSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()
    uploaded_by = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True  # Para que no se muestre en las respuestas
    )
    
    class Meta:
        model = ClientReport
        fields = '__all__'
        read_only_fields = ('upload_date',)

    def get_file_name(self, obj):
        return obj.filename()
# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .models import CustomUser, Appointment , ClientReport
from django.core.exceptions import ValidationError
from django.utils import timezone
from dateutil.relativedelta import *

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
        read_only_fields = ('professional',)  # Hacerlo solo de lectura
    
    def validate_datetime(self, value):
        # RF1.2 Validación de horario
        if value.hour < 9 or value.hour >= 20:
            raise serializers.ValidationError("Horario válido: 9:00 - 20:00")
        
        # Validar que sea en hora en punto
        if value.minute != 0 or value.second != 0:
            raise serializers.ValidationError("Debe ser una hora en punto exacta")
            
        # No permitir citas en el pasado
        if value < timezone.now():
            raise serializers.ValidationError("No puedes agendar citas en el pasado")
            
        return value
    
    def validate(self, data):
        user = data['user']
        appointment_type = data['type']
        datetime = data['datetime']
        
        # Validación de profesional asignado (existente)
        if appointment_type == 'nutricionista':
            professional = user.nutricionista
        elif appointment_type == 'entrenador':
            professional = user.entrenador
        else:
            professional = None
            
        if professional is None and appointment_type != 'clase':
            raise serializers.ValidationError(
                f"No tienes un {appointment_type} asignado"
            )
            
        data['professional'] = professional
        
        # Nueva validación de disponibilidad
        if professional:  # Solo aplica para nutricionista/entrenador
            conflicting_appointments = Appointment.objects.filter(
                professional=professional,
                datetime=datetime
            )
            
            # Excluir la propia cita en caso de actualización
            if self.instance:
                conflicting_appointments = conflicting_appointments.exclude(pk=self.instance.pk)
                
            if conflicting_appointments.exists():
                raise serializers.ValidationError(
                    "Este profesional ya tiene una cita programada en este horario"
                )
        
        # Validación adicional para clases
        if appointment_type == 'clase':
            # Verificar disponibilidad de la clase
            existing_class = Appointment.objects.filter(
                datetime=datetime,
                class_type=data['class_type']
            ).exists()
            
            if existing_class:
                raise serializers.ValidationError(
                    "Esta clase ya tiene participantes registrados en este horario"
                )
        # Validación de antelación para clases
        if appointment_type == 'clase':
            min_time = timezone.now() + relativedelta(hours=24)
            if datetime < min_time:
                raise serializers.ValidationError(
                    "Las clases deben reservarse con al menos 24h de antelación"
                )
        
        # Validación de límites semanales
        if appointment_type in ['nutricionista', 'entrenador']:
            week_number = datetime.isocalendar()[1]
            existing_count = Appointment.objects.filter(
                user=user,
                type=appointment_type,
                datetime__week=week_number,
                datetime__year=datetime.year
            ).count()
            
            limit = 1 if appointment_type == 'nutricionista' else 2
            if existing_count >= limit:
                raise serializers.ValidationError(
                    f"Límite semanal alcanzado ({limit} citas de {appointment_type})"
                )
        
        # Validación de capacidad de clases
        if appointment_type == 'clase':
            class_count = Appointment.objects.filter(
                class_type=data['class_type'],
                datetime=datetime
            ).count()
            if class_count >= 20:
                raise serializers.ValidationError(
                    "Clase llena (máximo 20 participantes)"
                )
            
        return super().validate(data)

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
        fields = ['id', 'name', 'surname', 'email', 'phone', 'role']


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
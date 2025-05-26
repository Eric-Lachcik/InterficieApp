from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
import os
from dateutil.relativedelta import *

class CustomUser(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('entrenador', 'Entrenador'),
        ('nutricionista', 'Nutricionista')
    )
    role = models.CharField(max_length=20, choices=ROLES, default='cliente')
    phone = models.CharField(max_length=20)
    weight = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    dni = models.CharField(max_length=9, unique=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    population = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    stature = models.FloatField(null=True, blank=True)
    staff = models.BooleanField(default=False)  # Campo para indicar si el usuario es un miembro del staff
    email = models.EmailField(max_length=50)  # Cambiado a EmailField para validación de correos electrónicos
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Campo para la fecha de registro

    # Campos para asignar entrenador y nutricionista
    entrenador = models.ForeignKey(
        'self',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clientes_asignados',  
        limit_choices_to={'role': 'entrenador'},  
        verbose_name='Entrenador asignado'
    )
    
    nutricionista = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_asignados',  
        limit_choices_to={'role': 'nutricionista'},  
        verbose_name='Nutricionista asignado'
    )

    # Añade estos campos al final de tu modelo
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_groups",  # Nombre único
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Nombre único
        related_query_name="customuser",
    )

    # Primer requisito de Robert
    def set_password(self, raw_password):
        # Hashing doble: SHA-256 + PBKDF2
        intermediate_hash = self._sha256_hash(raw_password)
        super().set_password(intermediate_hash) # Django aplica PBKDF2 aquí

    def _sha256_hash(self, password):
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, raw_password):
        # raw_password debe ser el texto plano del cliente
        intermediate_hash = self._sha256_hash(raw_password)
        return super().check_password(intermediate_hash)

class Appointment(models.Model):
    CLASS_TYPES = (
        ('step', 'Step'),
        ('bodypump', 'Bodypump'),
        ('spinning', 'Spinning'),
        ('zumba', 'Zumba'),
        ('crossfit', 'Crossfit'),
        ('pilates', 'Pilates'),
        ('yoga', 'Yoga')
    )
    
    TYPES = (
        ('nutricionista', 'Nutricionista'),
        ('entrenador', 'Entrenador'),
        ('clase', 'Clase Dirigida')
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citas_cliente')
    type = models.CharField(max_length=20, choices=TYPES)
    datetime = models.DateTimeField()
    professional = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='citas_profesional'
    )
    class_type = models.CharField(
        max_length=20, 
        choices=CLASS_TYPES, 
        null=True, 
        blank=True,
        verbose_name='Tipo de clase'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['professional', 'datetime'],
                name='unique_professional_time'
            ),
            models.UniqueConstraint(
                fields=['class_type', 'datetime'],
                name='unique_class_time',
                condition=models.Q(type='clase')
            )
        ]
    
    def get_week_number(self):
        return self.datetime.isocalendar()[1]
    
    def clean(self):
        # Validación RF1.2
        if self.datetime.hour < 9 or self.datetime.hour >= 21:
            raise ValidationError("Las citas deben ser entre las 9:00 y las 21:00")
        
        # Validación de minutos
        if self.datetime.minute != 0 or self.datetime.second != 0:
            raise ValidationError("Las citas deben ser en horas en punto (ej: 09:00, 10:00)")
            
        # Validación tipo de cita
        if self.type == 'clase' and not self.class_type:
            raise ValidationError("Debes seleccionar un tipo de clase")
            
        if self.type != 'clase' and self.class_type:
            raise ValidationError("El tipo de clase solo aplica para clases dirigidas")
    
    def __str__(self):
        return f"Cita de {self.user.name} - {self.get_type_display()} {self.datetime}"

class ClientReport(models.Model):
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='client_reports'
    )
    uploaded_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='uploaded_reports'
    )
    file = models.FileField(upload_to='client_reports/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('info', 'Información'),
        ('appointment', 'Cita'),
        ('report', 'Informe'),
        ('class', 'Clase')
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Notificación para {self.user.username} - {self.get_notification_type_display()}"
    
class EvolutionData(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='evolution_metrics'
    )
    date = models.DateField()  # Fecha de la medición
    weight = models.FloatField(help_text="Peso en kilogramos")  
    muscle_mass = models.FloatField(help_text="Masa muscular en porcentaje")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'date']  # Evita duplicados por fecha
        ordering = ['-date']
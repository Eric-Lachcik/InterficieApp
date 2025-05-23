from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfessionalSerializer, ClientReportSerializer, AppointmentSerializer
from rest_framework import generics
from .models import CustomUser, ClientReport, Appointment
from django.http import Http404
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TrainerListView(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    queryset = CustomUser.objects.filter(role='entrenador')

class NutritionistListView(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    queryset = CustomUser.objects.filter(role='nutricionista')

class UserDetailView(generics.RetrieveUpdateAPIView):  # Solo para obtener datos
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.kwargs['pk'])
        except CustomUser.DoesNotExist:
            raise Http404
    
    def perform_update(self, serializer):
        # Solo permitir actualizar ciertos campos
        allowed_fields = ['name', 'surname', 'weight', 'muscle_mass']
        serializer.save(**{
            k: v for k, v in serializer.validated_data.items()
            if k in allowed_fields
        })
        
class MyClientsView(APIView):
    def get(self, request):
        try:
            # Obtener parámetros del header
            user_id = request.META.get('HTTP_X_USER_ID')
            user_role = request.META.get('HTTP_X_USER_ROLE')
            print("User ID:", user_id)
            print("User Role:", user_role)
            if not user_id or not user_role:
                return Response(
                    {'error': 'Faltan headers requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar existencia del usuario
            user = CustomUser.objects.get(id=user_id)
            
            # Validar rol
            if user.role != user_role:
                return Response(
                    {'error': 'Rol no coincide con el usuario'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Obtener clientes según el rol
            if user_role == 'entrenador':
                clients = user.clientes_asignados.all()
            elif user_role == 'nutricionista':
                clients = user.pacientes_asignados.all()
            else:
                return Response(
                    {'error': 'Rol no válido'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = ProfessionalSerializer(clients, many=True)
            return Response(serializer.data)
            
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ClientReportViewSet(viewsets.ModelViewSet):
    queryset = ClientReport.objects.all()
    serializer_class = ClientReportSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Obtener el ID del usuario desde los datos validados
        user_id = serializer.validated_data.get('uploaded_by')
        try:
            # user = CustomUser.objects.get(id=user_id)
            serializer.save(uploaded_by=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError({"uploaded_by": "Usuario no encontrado"})

    def get_queryset(self):
        # Filtrar por cliente si se provee el parámetro
        client_id = self.request.query_params.get('client')
        if client_id:
            return ClientReport.objects.filter(client=client_id)
        return ClientReport.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    
    def get_queryset(self):
        # Obtener citas por usuario desde parámetros (ej: ?user=1)
        user_id = self.request.query_params.get('user')
        if user_id:
            return Appointment.objects.filter(user__id=user_id)
        return Appointment.objects.all()
    
    def perform_create(self, serializer):
        # Asignar usuario desde los datos enviados
        user_id = self.request.data.get('user')
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer.save(user=user)
        except CustomUser.DoesNotExist:
            pass  # O manejar el error según necesidades

class AvailableProfessionalsView(APIView):    
    def get(self, request):
        role = request.query_params.get('role')
        if not role:
            return Response(
                {"error": "Parámetro 'role' requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        professionals = CustomUser.objects.filter(role=role)
        serializer = ProfessionalSerializer(professionals, many=True)
        return Response(serializer.data)
    
class ProfessionalAvailabilityView(APIView):
    def get(self, request, professional_id):
        now = timezone.localtime()
        next_day = now + timedelta(days=1)
        
        # Horario base del día siguiente (9:00 a 21:00)
        base_date = next_day.replace(
            hour=9, minute=0, second=0, microsecond=0
        )
        end_date = base_date.replace(hour=20, minute=0)  # Nueva hora límite
        # Generar slots válidos (24h de antelación)
        valid_slots = []
        current_slot = base_date
        
         # Generar hasta las 20:00 inclusive
        while current_slot <= end_date:
            # Verificar antelación mínima de 24h
            if current_slot > now + timedelta(hours=24):
                valid_slots.append(current_slot)
            current_slot += timedelta(hours=1)
            
        # Filtrar citas existentes
        existing_appointments = Appointment.objects.filter(
            professional=professional_id,
            datetime__date=base_date.date()
        ).values_list('datetime', flat=True)
        
        available_slots = [
            slot for slot in valid_slots
            if slot not in existing_appointments
        ]
        
        return Response({
            'available_slots': available_slots
        })
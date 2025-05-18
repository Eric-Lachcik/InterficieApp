from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfessionalSerializer, ClientReportSerializer
from rest_framework import generics
from .models import CustomUser, ClientReport
from django.http import Http404
from rest_framework.exceptions import ValidationError

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

class UserDetailView(generics.RetrieveAPIView):  # Solo para obtener datos
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    
    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.kwargs['pk'])
        except CustomUser.DoesNotExist:
            raise Http404
        
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
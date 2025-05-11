from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfessionalSerializer
from rest_framework import generics
from .models import CustomUser
from django.http import Http404

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
        
# class UserDetailView(APIView):
    # def get(self, request):
    #     try:
    #         user = CustomUser.objects.get(pk=request.data)
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data)
    #     except CustomUser.DoesNotExist:
    #         return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
class UserDetailView(generics.RetrieveAPIView):  # Solo para obtener datos
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    
    def get_object(self):
        try:
            return CustomUser.objects.get(pk=self.kwargs['pk'])
        except CustomUser.DoesNotExist:
            raise Http404
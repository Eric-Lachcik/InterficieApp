from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfessionalSerializer
from rest_framework import generics
from .models import CustomUser

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
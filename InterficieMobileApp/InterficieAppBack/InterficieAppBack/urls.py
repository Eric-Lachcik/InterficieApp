"""
URL configuration for InterficieAppBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers
from FitCoreBack.serializers import SecureTokenObtainPairSerializer 
from FitCoreBack.views import RegisterView, TrainerListView, NutritionistListView, UserDetailView, MyClientsView, ClientReportViewSet, AppointmentViewSet, AvailableProfessionalsView, ProfessionalAvailabilityView, NotificationViewSet, EvolutionCSVUploadView, EvolutionDataView


router = routers.DefaultRouter()
router.register(r'client-reports', ClientReportViewSet, basename='client-reports')
router.register(r'appointments', AppointmentViewSet, basename='appointments')
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = SecureTokenObtainPairSerializer

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # Autenticación
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),

    # Usuarios
    path('api/users/<str:pk>/' , UserDetailView.as_view()),  

    # Staff
    path('api/trainers/', TrainerListView.as_view(), name='trainers-list'),
    path('api/nutritionists/', NutritionistListView.as_view(), name='nutritionists-list'),
    path('api/my-clients/', MyClientsView.as_view(), name='my-clients'),

    # Informes (usando el router)
    path('api/', include(router.urls)),

    # Citas
    path('api/professionals/', AvailableProfessionalsView.as_view()),
    path('api/availability/<int:professional_id>/', ProfessionalAvailabilityView.as_view()),

    # Notificaciones
    path('api/notifications/', NotificationViewSet.as_view({'get': 'list'}), name='notifications-list'),
    path('api/notifications/<int:pk>/mark-read/', NotificationViewSet.as_view({'patch': 'mark_as_read'}), name='mark-notification-read'),
    path('api/notifications/mark-all-read/', NotificationViewSet.as_view({'post': 'mark_all_read'}), name='mark-all-read'),

    # Graficos
    path('api/evolution/<int:user_id>/', EvolutionDataView.as_view(), name='evolution-data'),
    path('api/evolution/upload/', EvolutionCSVUploadView.as_view(), name='evolution-upload'),
]
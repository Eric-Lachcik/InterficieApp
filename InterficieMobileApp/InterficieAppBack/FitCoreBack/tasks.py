from celery import shared_task
from django.db import transaction
from .models import Appointment
from django.db.models import F
from django.db import models

@shared_task
@transaction.atomic
def process_class_reservation(class_type, datetime, user_ids):
    
    # Verificar disponibilidad con bloqueo atómico
    appointments = Appointment.objects.select_for_update().filter(
        class_type=class_type,
        datetime=datetime
    )
    
    if appointments.count() >= 20:
        return {'status': 'error', 'message': 'Clase llena'}
    
    # Crear reservas usando bulk_create para eficiencia
    new_appointments = [
        Appointment(
            user_id=user_id,
            type='clase',
            class_type=class_type,
            datetime=datetime
        ) for user_id in user_ids
    ]
    
    created = Appointment.objects.bulk_create(new_appointments)
    return {'status': 'success', 'created': len(created)}
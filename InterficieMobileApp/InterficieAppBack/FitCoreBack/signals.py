from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClientReport, Appointment, Notification
from dateutil.relativedelta import *

@receiver(post_save, sender=ClientReport)
def create_report_notification(sender, instance, created, **kwargs):
    if created:
        # Notificar al cliente
        Notification.objects.create(
            user=instance.client,
            message=f"Nuevo informe subido por {instance.uploaded_by.name}",
            notification_type='report',
            related_object_id=instance.id
        )

@receiver(post_save, sender=Appointment)
def create_appointment_notification(sender, instance, created, **kwargs):
    if created:
        # Notificar al profesional
        if instance.professional:
            # Añadir 2 horas manualmente
            # local_time = instance.datetime + relativedelta(hours=2)
            # message = f"Nueva cita con {instance.user.name} el {local_time.strftime('%d/%m a las %H:%M')}"
            # Notification.objects.create(
            #     user=instance.professional,
            #     message=message,
            #     notification_type='appointment',
            #     related_object_id=instance.id
            # )
            Notification.objects.create(
                user=instance.professional,
                message=f"Nueva cita con {instance.user.name} el {instance.datetime.strftime('%d/%m a las %H:%M')}",
                notification_type='appointment',
                related_object_id=instance.id
            )
        
        # Notificar al cliente
        Notification.objects.create(
            user=instance.user,
            message=f"Cita confirmada con {instance.professional.name if instance.professional else 'clase'}",
            notification_type='appointment',
            related_object_id=instance.id
        )
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Incident, IncidentAcknowledgement

@receiver(post_save, sender=Incident)
def create_acknowledgements_for_incident(sender, instance, created, **kwargs):
    if created:
        # On récupère le groupe normal_user
        try:
            normal_group = Group.objects.get(name='normal_user')
            normal_users = normal_group.user_set.all()
            for user in normal_users:
                IncidentAcknowledgement.objects.create(
                    incident=instance,
                    user=user,
                    seen=False
                )
        except Group.DoesNotExist:
            pass

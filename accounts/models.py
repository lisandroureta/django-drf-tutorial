from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # 1. Relación 1 a 1: Cada Usuario tiene UN Perfil exacto.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 2. Relación Muchos a Muchos: Un perfil sigue a muchos usuarios.
    # 'symmetrical=False' es CLAVE: Si yo te sigo, no significa que tú me sigas (como Twitter/Instagram).
    # Si fuera True, sería como Facebook (Amigos).
    following = models.ManyToManyField(User, related_name='followers', blank=True, symmetrical=False)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# --- SEÑALES (Magia Automática) ---
# Queremos que cuando se cree un User, se cree su Profile automáticamente.
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
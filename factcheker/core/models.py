from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Extend the User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate_limit = models.IntegerField(default=2)
    usage = models.IntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username + " - " + str(self.usage) + "/" + str(self.rate_limit) + " - " + str(self.last_used)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.translation import gettext as _
STATUS_CHOICES = (
    (1, _('Enseignant')),
    (2, _('Responsable module')),
    (3, _('Chef de departement')),
    (4, _('Administrateur')))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return f'{self.user.username} Profil'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)


        
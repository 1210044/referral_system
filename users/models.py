from random import choices
from string import ascii_letters, digits
from django.db import models


def set_invite_code(instance):
    return instance.invite_code


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    activated_invite_code = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET(set_invite_code), 
        related_name='invitees', to_field='invite_code'
        )

    class Meta:
        db_table = 'users' 

    @staticmethod
    def generate_invite_code():
        while True:
            invite_code = ''.join(choices(ascii_letters + digits, k=6))
            if not User.objects.filter(invite_code=invite_code).exists():
                return invite_code

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

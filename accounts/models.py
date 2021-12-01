from django.contrib.admin import display
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='联系电话')

    @display(description='姓名')
    def get_full_name(self):
        """
        Return the last_name plus the first_name
        """
        full_name = f'{self.last_name}{self.first_name}'
        return full_name.strip()

    def __str__(self):
        return self.username

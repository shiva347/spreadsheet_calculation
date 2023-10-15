from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampModel(models.Model):
    added_by = models.CharField(max_length=250, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    last_modified_by = models.CharField(max_length=250, null=True, blank=True)
    last_modified_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

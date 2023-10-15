from django.db import models
from jsonfield import JSONField

from users.models import User, TimeStampModel


class FileRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='spread_sheets/')

    def __str__(self):
        return f'{self.user} - {self.request_time}'


class CalculationResult(TimeStampModel):
    request = models.ForeignKey(FileRequest, on_delete=models.RESTRICT)
    result = models.DecimalField(max_digits=15, decimal_places=3)
    errors = JSONField(null=True, blank=True)

    def __str__(self):
        return self.result


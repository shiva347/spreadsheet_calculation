from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.FileRequest)
admin.site.register(models.CalculationResult)

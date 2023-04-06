from django.db import models

class mangosModel(models.Model):
    imagen = models.ImageField(upload_to="mangos", null=False)
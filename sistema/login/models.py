from django.db import models

class Usuario(models.Model):
    usuario = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario


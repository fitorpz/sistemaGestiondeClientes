from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class panelAdmin(models.Model):
    OPCIONES_DE_PLAN = [
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]
    cuenta=models.CharField(max_length=10)
    contrasena=models.CharField(max_length=10)
    fechaInicio=models.DateTimeField(auto_now_add=True) #Establece la fecha al momento de la creación
    plan = models.CharField(max_length=20, choices=OPCIONES_DE_PLAN, default='mensual')
    fechaUltimoPago=models.DateTimeField(null=True, blank=True) #Puede ser nulo y editable
    



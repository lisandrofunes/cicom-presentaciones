from django.db import models
from django.forms import IntegerField

class Archivo(models.Model):
    nombre = models.CharField(max_length=100)
    archivo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.nombre

class Presentacion(models.Model):
    titulo = models.CharField(max_length=100)
    archivos = models.ManyToManyField(Archivo, through='DetallePresentacion')
    tiempo = models.IntegerField(default=20)

    def __str__(self):
        return self.titulo

class DetallePresentacion(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()

    def __str__(self):
        return self.archivo.nombre


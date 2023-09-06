from django.contrib import admin

from  .models import  Archivo, Presentacion, DetallePresentacion

# Register your models here.

admin.site.register(Archivo)
admin.site.register(Presentacion)
admin.site.register(DetallePresentacion)

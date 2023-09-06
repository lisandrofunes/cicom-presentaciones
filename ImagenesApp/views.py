from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Archivo, DetallePresentacion, Presentacion
from django.views import View
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView


class CargarArchivoView(View):
    def post(self, request):
        nombre = request.POST.get('nombre')
        archivo = request.FILES.get('archivo')  # Obtener el archivo de la solicitud POST
        # tipo_mimetype = archivo.content_type  # Obtener el tipo MIME

        # nuevo_archivo = Archivo(nombre=nombre, archivo=archivo, tipo_mimetype=tipo_mimetype)
        nuevo_archivo = Archivo(nombre=nombre, archivo=archivo)
        nuevo_archivo.save()

        return HttpResponse("Archivo cargado exitosamente")

    def get(self, request):
        return render(request, 'cargar_archivo.html')



class ArchivoCreate(CreateView):
    model = Archivo
    # permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    template_name =  'ImagenesApp/archivo_form.html'
    success_url = reverse_lazy('index')



class CrearPresentacionView(View):
    def get(self, request):
        archivos = Archivo.objects.all()  # Obtener archivos disponibles para seleccionar
        return render(request, 'ImagenesApp/presentacion_form.html', {'archivos': archivos})

    def post(self, request):
        titulo = request.POST.get('titulo')
        tiempo = request.POST.get('tiempo')
        archivos_seleccionados = request.POST.getlist('archivos[]')

        nueva_presentacion = Presentacion(titulo=titulo, tiempo=tiempo)
        nueva_presentacion.save()

        for i, archivo_id in enumerate(archivos_seleccionados, start=1):
            archivo = Archivo.objects.get(id=archivo_id)
            detalle = DetallePresentacion(presentacion=nueva_presentacion, archivo=archivo, orden=i)
            detalle.save()

        return HttpResponse("Presentación creada exitosamente")


class PresentacionDeleteView(DeleteView):
    model = Presentacion
    template_name = 'ImagenesApp/presentacion_delete.html'  
    success_url = reverse_lazy('index')  

def index(request):
    return render(request, 'ImagenesApp/index.html')



# def crear_presentacion(request):
#     if request.method == 'POST':
#         titulo = request.POST.get('titulo')
#         archivo_ids = request.POST.getlist('archivos')  # Obtener una lista de IDs de archivos seleccionados

#         nueva_presentacion = Presentacion(titulo=titulo)
#         nueva_presentacion.save()

#         for index, archivo_id in enumerate(archivo_ids):
#             archivo = Archivo.objects.get(pk=archivo_id)
#             DetallePresentacion.objects.create(presentacion=nueva_presentacion, archivo=archivo, orden=index)

    # Resto de tu vista...

from django.views import generic

class ArchivoListView(generic.ListView):
    model = Archivo
    paginate_by = 10
    
class PresentacionListView(generic.ListView):
    model = Presentacion
 
class MostrarPresentacionView(View):
    def get(self, request, titulo):
        try:
            presentacion = Presentacion.objects.get(titulo=titulo)
        except Presentacion.DoesNotExist:
            return HttpResponse("La presentación no existe")

        detalles = DetallePresentacion.objects.filter(presentacion=presentacion).order_by('orden')
        archivos = [detalle.archivo for detalle in detalles]

        context = {
            'presentacion': presentacion,
            'archivos': archivos,
            'duracion': presentacion.tiempo
        }

        return render(request, 'ImagenesApp/presentacion_vista.html', context)

def deleteArchivo(request,pk):
     archivo=get_object_or_404(Archivo,pk=pk)
     archivo.delete()
        
     return redirect ('imagenes:archivo-list')
        
class EditarArchivo(UpdateView):
    modelo=Archivo
    
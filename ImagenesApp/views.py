from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy,reverse
from .models import Archivo, DetallePresentacion, Presentacion
from django.views import View, generic
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import EditarArchivos
from django.http import HttpResponseRedirect


# --- ARCHIVOS ---

@login_required
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

@method_decorator(login_required, name='dispatch')
class ArchivoCreate(CreateView):
    model = Archivo
    # permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    template_name =  'ImagenesApp/archivo_form.html'
    success_url = reverse_lazy('imagenes:archivo-list')


@method_decorator(login_required, name='dispatch')
class ArchivoListView(generic.ListView):
    model = Archivo
    paginate_by = 10

@login_required
def deleteArchivo(request,pk):
     archivo=get_object_or_404(Archivo,pk=pk)
     archivo.delete()
        
     return redirect ('imagenes:archivo-list')


@method_decorator(login_required, name='dispatch') 
class EditarArchivo(UpdateView):
    model = Archivo
    form_class = EditarArchivos
    template_name = 'ImagenesApp/editar_archivo.html'  
    success_url = reverse_lazy('imagen:archivo-list')
        
# --- PRESENTACIONES ---

@method_decorator(login_required, name='dispatch')
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


#-------------Chequear------------

@method_decorator(login_required, name='dispatch')
class PresentacionEditView(UpdateView):
    model = Presentacion
    template_name = 'ImagenesApp/presentacion_edit.html'
    fields = ['titulo', 'tiempo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archivos_disponibles'] = Archivo.objects.exclude(detallepresentacion__presentacion=self.object)
        return context

    def form_valid(self, form):
        # Guarda la presentación
        self.object = form.save()

        # Procesa los archivos seleccionados y los relaciona con la presentación
        archivos_seleccionados = self.request.POST.getlist('archivos')
        for archivo_id in archivos_seleccionados:
            archivo = Archivo.objects.get(id=archivo_id)
            # Crea una relación entre la presentación y el archivo
            DetallePresentacion.objects.create(presentacion=self.object, archivo=archivo)

        return redirect ('imagenes:presentacion-list')   
# ------------------------------------



@method_decorator(login_required, name='dispatch')
class PresentacionListView(generic.ListView):
    model = Presentacion
 
# @method_decorator(login_required, name='dispatch')
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

    
@method_decorator(login_required, name='dispatch')
class PresentacionDeleteView(DeleteView):
    model = Presentacion
    template_name = 'ImagenesApp/presentacion_delete.html'  
    success_url = reverse_lazy('index')  

def index(request):
    return render(request, 'ImagenesApp/index.html')


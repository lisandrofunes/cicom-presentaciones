from django import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .forms import LoginForm

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='imagenes'
urlpatterns = [ 
    #  path('', CargarArchivoView.as_view(), name='cargar_archivo'),
    path('archivo-create/', views.ArchivoCreate.as_view(), name='archivo-create'),
    path('', views.PresentacionListView.as_view(), name='index'),
    path('archivos/', views.ArchivoListView.as_view(), name='archivo-list'),
    path('presentacion-create/', views.CrearPresentacionView.as_view(), name='presentacion-create'),
    path('presentacion-vista/<str:titulo>', views.MostrarPresentacionView.as_view(), name='presentacion-vista'),
    path('presentacion-delete/<int:pk>', views.PresentacionDeleteView.as_view(), name='presentacion-delete'),
    path('<int:pk>/delete', views.deleteArchivo, name='delete'),
    path('login/', auth_views.LoginView.as_view(template_name='ImagenesApp/login.html',authentication_form=LoginForm),name='login'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
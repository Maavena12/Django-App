from django.urls import path  
from . import views  
from django.conf import settings  
from django.conf.urls.static import static 

urlpatterns = [  
    path('', views.lista_gastos, name='lista_gastos'),
    path('login/', views.login_view, name='login'),  
    path('registro/', views.registro, name='registro'),
    path('agregar/', views.agregar_gasto, name='agregar_gasto'),
    path('perfil/', views.perfil, name='perfil'),
    path('borrar-cuenta/', views.borrar_cuenta, name='borrar_cuenta'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('logout/', views.custom_logout, name='logout'),
    path('pagar/<int:gasto_id>/', views.pagar_gasto, name='pagar_gasto'),
    path('detalle/<int:gasto_id>/', views.gasto_detalle, name='gasto_detalle'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

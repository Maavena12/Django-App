from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from bills.forms import GastoForm, PaymentForm, RegistroForm, UsuarioForm  
from .models import Gasto, Usuario  
from django.db.models import Sum, Max
from django.db.models.functions import TruncMonth 
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout 
from .forms import LoginForm 

def lista_gastos(request):  
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
    gastos = Gasto.objects.filter(usuario=usuario)
    total_gastos = sum(gasto.cantidad for gasto in gastos)
    return render(request, 'bills/lista_gastos.html', {'gastos': gastos, 'total_gastos': total_gastos})

def login_view(request):  
    if request.method == 'POST':  
        form = LoginForm(request.POST)  
        if form.is_valid():  
            correo = form.cleaned_data['correo']  
            contraseña = form.cleaned_data['contraseña']  
            usuario = Usuario.objects.get(correo=correo)  
            if (contraseña == usuario.contraseña):
                request.session['usuario_id'] = usuario.id
                messages.success(request, 'Inicio de Sesión Exitosa.') 
                return redirect('/gastos')
            else:  
                messages.error(request, 'Credenciales incorrectas.')  
    else:  
        form = LoginForm()  

    return render(request, 'bills/login.html', {'form': form})  


def registro(request):  
    if request.method == 'POST':  
        form = RegistroForm(request.POST)  
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Cuenta creada con éxito. Puedes iniciar sesión.')  
            return redirect('login')
    else:  
        form = RegistroForm()  

    return render(request, 'bills/registro.html', {'form': form}) 

def agregar_gasto(request):  
    if request.method == 'POST':  
        form = GastoForm(request.POST)  
        if form.is_valid():  
            gasto = form.save(commit=False)  
            usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])
            gasto.usuario = usuario
            gasto.save()   
            messages.success(request, 'Gasto agregado exitosamente.')  
            return redirect('/gastos')
    else:  
        form = GastoForm()  
    
    return render(request, 'bills/agregar_gasto.html', {'form': form}) 

def obtener_nombre_mes(fecha):  
    return calendar.month_name[fecha.month] 


def perfil(request): 
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])  
    gastos_mensuales = (  
        Gasto.objects.filter(usuario=usuario)  
        .annotate(mes=TruncMonth('fecha_registro'))  
        .values('mes')  
        .annotate(total_gastado=Sum('cantidad'), max_gasto=Max('cantidad'))  
        .order_by('mes')  
    ) 

    resumen_gastos = {gasto['mes']: gasto for gasto in gastos_mensuales}  
      
    for i in range(len(gastos_mensuales) - 1):  
        mes_actual = gastos_mensuales[i]  
        mes_anterior = gastos_mensuales[i + 1]
        if mes_actual['total_gastado'] > 0:  
            porcentaje_cambio = ((mes_actual['total_gastado'] - mes_anterior['total_gastado']) / mes_anterior['total_gastado']) * 100  
        else:  
            porcentaje_cambio = 0 
        
        mes_actual['porcentaje'] = porcentaje_cambio
    return render(request, 'bills/perfil.html', {'user': usuario, 'gastos_mensuales': gastos_mensuales})

def borrar_cuenta(request):  
    usuario = get_object_or_404(Usuario, id=request.session['usuario_id'])  
    if request.method == 'POST':  
        usuario.delete()  
        return redirect('login')
    return render(request, 'bills/confirmar_borrar_cuenta.html', {'user': usuario})

def editar_perfil(request):  
    user = get_object_or_404(Usuario, id=request.session['usuario_id'])  # Obtén el usuario actual  
    if request.method == 'POST':  
        form = UsuarioForm(request.POST, instance=user)  
        if form.is_valid():  
            # Solo actualizar la contraseña si se proporciona una nueva  
            nueva_contrasena = form.cleaned_data.get("nueva_contrasena")  
            if nueva_contrasena:  
                user.contraseña = nueva_contrasena  # Almacena la contraseña como un hash  

            form.save()  # Guarda la información actualizada  
            return redirect('perfil')  # Redirecciona a la vista de perfil o donde desees  
    else:  
        form = UsuarioForm(instance=user)  # Carga el formulario con los datos del usuario actual  

    return render(request, 'bills/editar_perfil.html', {'form': form}) 

def custom_logout(request):  
    logout(request)  
    return redirect('bills/login.html')

def pagar_gasto(request, gasto_id):  
    gasto = get_object_or_404(Gasto, id=gasto_id) 
    
    if request.method == 'POST':  
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():  
            gasto.info = form.cleaned_data['info']  
            if form.cleaned_data.get('imagen'):  
                gasto.imagen = form.cleaned_data['imagen']
            gasto.pagado = True  
            gasto.save() 
            messages.success(request, 'Gasto Pagado exitosamente.')  
            return redirect('/gastos')
    else:  
        form = PaymentForm() 

    return render(request, 'bills/pagar_gasto.html', {'form': form, 'gasto': gasto}) 

def gasto_detalle(request, gasto_id):  
    gasto = get_object_or_404(Gasto, id=gasto_id) 
    return render(request, 'bills/gasto_detalle.html', {'gasto': gasto})
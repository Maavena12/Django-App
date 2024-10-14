from django.shortcuts import get_object_or_404, redirect, render  
from django.urls import reverse  
from django.contrib.auth.decorators import login_required

from bills.models import Gasto, Usuario  

@login_required(login_url='gastos/login')  
def home(request):  
    usuario_id = request.session.get('usuario_id')  
    if usuario_id is None:   
        return redirect('gastos/login')  # O cualquier otra acción que desees  
    usuario = get_object_or_404(Usuario, id=usuario_id)  
    gastos = Gasto.objects.filter(usuario=usuario)  
    return render(request, 'bills/lista_gastos.html', {'gastos': gastos})  

def redirect_to_login(request):  
    # Esta vista redirigirá a la página de inicio de login si no hay sesión activa  
    return redirect(reverse('login')) 
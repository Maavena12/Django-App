# forms.py  
from django import forms  
from .models import Gasto, Usuario 

class LoginForm(forms.Form):  
    correo = forms.EmailField(label='Correo', max_length=100)  
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput) 

class RegistroForm(forms.ModelForm):  
    class Meta:  
        model = Usuario  
        fields = ['nombre', 'apellido', 'correo', 'contraseña', 'nombre_usuario']  
        widgets = {  
            'contraseña': forms.PasswordInput(),  
        }

class GastoForm(forms.ModelForm):  
    class Meta:  
        model = Gasto  
        fields = ['nombre', 'cantidad', 'categoria', 'fecha_caducidad', 'mensual']  
        widgets = {  
            'fecha_caducidad': forms.widgets.DateInput(attrs={'type': 'date'}),  
        } 


class UsuarioForm(forms.ModelForm):  
    nueva_contrasena = forms.CharField(  
        max_length=100,   
        required=False,   
        widget=forms.PasswordInput,   
        label="Nueva Contraseña"  
    )  
    confirmar_contrasena = forms.CharField(  
        max_length=100,   
        required=False,   
        widget=forms.PasswordInput,   
        label="Confirmar Nueva Contraseña"  
    )  

    class Meta:  
        model = Usuario  
        fields = ['nombre', 'apellido', 'correo', 'nombre_usuario', 'nueva_contrasena', 'confirmar_contrasena']  

    def clean(self):  
        cleaned_data = super().clean()  
        nueva_contrasena = cleaned_data.get("nueva_contrasena")  
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")  

        # Verificar si ambas contraseñas coinciden si se ingresa una nueva contraseña  
        if nueva_contrasena and nueva_contrasena != confirmar_contrasena:  
            self.add_error('confirmar_contrasena', "Las contraseñas no coinciden.")  

class PaymentForm(forms.ModelForm):  
    class Meta:  
        model = Gasto 
        fields = ['info', 'imagen']  
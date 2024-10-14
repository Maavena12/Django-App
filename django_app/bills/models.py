from django.db import models
    
class Usuario(models.Model):  
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)  
    apellido = models.CharField(max_length=100)  
    correo = models.EmailField(unique=True)  
    contraseña = models.CharField(max_length=100)  # Considera usar un hash para seguridad  
    nombre_usuario = models.CharField(max_length=100, unique=True)  

    def __str__(self):  
        return f"{self.nombre} {self.apellido} ({self.nombre_usuario})"  
    
class Gasto(models.Model):   
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)  
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)  
    categoria = models.CharField(max_length=100)  
    fecha_registro = models.DateField(auto_now_add=True) 
    fecha_caducidad = models.DateField()  
    mensual = models.BooleanField(default=False) 
    pagado = models.BooleanField(default=False)
    info = models.CharField(max_length=100, null=True)
    imagen = models.ImageField(upload_to='gastos/', blank=True, null=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='gastos', null=True) 

    def __str__(self):  
        return f"{self.nombre}: {self.cantidad} en {self.fecha_registro}"
    


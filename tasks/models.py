from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)#Campo de texto tipo varchar
    description = models.TextField(blank=True)#Campo de texto tipo longtxt
    created = models.DateTimeField(auto_now_add=True)#Campo de fecha con el auto_now_add te agrega la fecha de creado
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#Para eliminar las tareas junto con el usuario

    def __str__(self):#Metodo para que muestre el titulo de la tarea en el admin y cualquier otro sitio
        return self.title + ' - by ' + self.user.username
    
    

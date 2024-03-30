from django.contrib import admin
from .models import Task, Avatar


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_de_creacion', )

# Registra el modelo con la clase de administración personalizada
admin.site.register(Task, TaskAdmin)
admin.site.register(Avatar)

from django.contrib import admin

# Register your models here.
from .models import (Perfil, Medico, HistorialClinico, PerfilLipidico, Paciente, RegressionLinearModel, FileToProcess)

admin.site.register(Perfil)
admin.site.register(Medico)
admin.site.register(HistorialClinico)
admin.site.register(PerfilLipidico)
admin.site.register(Paciente)
admin.site.register(RegressionLinearModel)
admin.site.register(FileToProcess)

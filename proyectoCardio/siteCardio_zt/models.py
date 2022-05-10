import os
import ast
import pandas as pd
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pandas as pd
from django.conf import settings


# Create your models here.
CHOICE_GENERO = (('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro'),)
CHOICE_RAZA = (('Mestizo', 'Mestizo'), ('Montubio', 'Montubio'), ('Indígena', 'Indígena'),
                 ('Quichua', 'Quichua'), ('Shuar', 'Shuar'), ('Asiáticos', 'Asiáticos'),
                 ('Afroecuatoriano', 'Afroecuatoriano'), ('Otro', 'Otro'),)


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=15, null=False)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono_personal = models.CharField(max_length=12, blank=True, null=True)
    genero = models.CharField(null=True, blank=True, max_length=10, choices=CHOICE_GENERO)
    cuentaVerif = models.NullBooleanField(default=False)
    id_usuario = models.OneToOneField(User)

    def __str__(self):
        return '%s - %s' % (self.id_usuario, self.id_usuario.username)

    class Meta:
        verbose_name_plural = 'Perfiles'


class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=10, blank=True, null=True)
    prioridad = models.IntegerField(null=True)
    disponibilidad = models.NullBooleanField(default=True)
    id_perfil = models.ForeignKey(Perfil, related_name='medicos')
    inf_adicional = models.CharField(max_length=20)

    def __str__(self):
        return '%s' % self.titulo

    class Meta:
        verbose_name_plural = 'Medicos'

    def __unicode__(self):
        return '%s' % self.id_medico


class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, related_name='PacientePerfil')
    hta = models.BooleanField(default=False)
    dmt2 = models.BooleanField(default=False)
    raza = models.CharField(null=True, blank=True, max_length=15, choices=CHOICE_RAZA)

    def __str__(self):
        return '%s' % self.id_perfil.cedula

    class Meta:
        verbose_name_plural = 'Pacientes'

    def __unicode__(self):
        return '%s' % self.id_paciente


class HistorialClinico(models.Model):
    id_hc = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Perfil, related_name='HistorialClinicoPaciente')
    last_update = models.DateTimeField(default=datetime.now, blank=True)
    create_update = models.DateTimeField(default=datetime.now, blank=False, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.id_hc, self.id_paciente.cedula)

    class Meta:
        verbose_name_plural = 'HistoriasClincias'

    def __unicode__(self):
        return '%s' % self.id_paciente


class PerfilLipidico(models.Model):
    id_pl = models.AutoField(primary_key=True)
    id_hc = models.ForeignKey(HistorialClinico, related_name='PerfilHistorialClinico')
    date = models.DateField(default=datetime.now, null=False)
    col_t = models.FloatField(null=True, blank=True)
    ldl_c = models.FloatField(null=True, blank=True)
    hdl_c = models.FloatField(null=True, blank=True)
    col_no_hdl = models.FloatField(null=True, blank=True)
    trigliceridos = models.FloatField(null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.id_hc, self.id_hc.id_hc)

    class Meta:
        verbose_name_plural = 'PerfilesLipidico'

    def __unicode__(self):
        return '%s' % self.id_pl


class FileToProcess(models.Model):
    id_file = models.AutoField(primary_key=True)
    file_name = models.CharField(null=False, max_length=60)
    file_path = models.CharField(null=False, max_length=200)
    description = models.TextField(null=True)
    columns = models.TextField(null=False)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '%s, %s' % (self.id_file, self.file_name)

    class Meta:
        verbose_name_plural = 'Archivos a procesar'

    def __unicode__(self):
        return '%s' % self.id_file

    def get_absolute_path(self):
        return os.path.join(settings.BASE_DIR, self.file_path)

    def get_df(self):
        print("path: {}".format(self.get_absolute_path()))
        return pd.read_csv(self.get_absolute_path())


class RegressionLinearModel(models.Model):
    id_model = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=60)
    model_path = models.CharField(null=True, max_length=100)
    file_name = models.CharField(null=True, max_length=60)
    coef = models.TextField(null=False)
    accuracy = models.TextField(null=True, default="0")
    intercept = models.TextField(null=False)
    dependent_var = models.TextField(null=False)
    independent_var = models.TextField(null=False)
    description = models.TextField(null=True)
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.BooleanField(default=True)
    id_file = models.ForeignKey(FileToProcess, related_name="Archivo")

    def __str__(self):
        return '%s, %s, date: %s' % (self.id_model, self.name, self.create_date)

    class Meta:
        verbose_name_plural = 'Regression Linear Model'

    def __unicode__(self):
        return '%s' % self.id_model

    def config_columns(self):
        self.dependent_var = ast.literal_eval(self.dependent_var)
        self.independent_var = ast.literal_eval(self.independent_var)


class PredictionsResult(models.Model):
    id = models.AutoField(primary_key=True)
    id_regresion_lm = models.ForeignKey(RegressionLinearModel, related_name="LineraMOdel")
    prediction = models.CharField(null=False, max_length=5)
    coef = models.CharField(null=False, max_length=5)
    intercept = models.CharField(null=False, max_length=5)

    def __str__(self):
        return 'predict: %s, coef: %s, intercept: %s' % (self.prediction, self.coef, self.intercept)

    def get_data(self):
        return pd.read_csv(self.id_regresion_lm.file_name)

from django.forms import Form
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

class FormLogin(Form):
    username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'input100'}))
    password = forms.CharField(label='', required=True,  widget=forms.PasswordInput(attrs={'class': 'input100'}))

    '''class Meta:
        model = Usuario'''

    def clean(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            users = User.objects.filter(email=username)
            if len(users) > 0:
                user = authenticate(username=users[0].username, password=password)
        invalido = forms.ValidationError('Nombre de usuario o clave inválidos', )

        if user is None:
            print('usernameeeeeeee')
            # raise forms.ValidationError('Nombre de usuario o clave inválidos')
            self.add_error('password', invalido)

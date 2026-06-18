from app.familiares.models import Familiar
from django import forms
from app.usuario.models import Usuario


class FamiliarCreacionForm(forms.ModelForm):
    username = forms.CharField(label='Código de familiar', max_length=10)
    first_name = forms.CharField(label='Nombres', max_length=100)
    apellido_p = forms.CharField(label='Apellido paterno', max_length=100)
    apellido_m = forms.CharField(label='Apellido materno', max_length=100)
    parentesco = forms.CharField(label='Parentesco', max_length=50)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput, max_length=10)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, max_length=10)
     
    class Meta:
        model = Familiar
        exclude = ['usuario', 'nombre', 'apellido_paterno', 'apellido_materno', 'parentesco', 'codFamiliar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border-b-2 border-gray-300 focus:border-blue-500 px-2 py-2'
            })
        


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(codUsuario=username).exists():
            raise forms.ValidationError('Ya existe un usuario con este codigo')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = Usuario(
            codUsuario=username,
            password=password,)
        user.save()

        familiar = super().save(commit=False)
        familiar.codFamiliar = username 
        familiar.usuario = user

        familiar.nombre = self.cleaned_data['first_name']
        familiar.apellido_paterno = self.cleaned_data['apellido_p']
        familiar.apellido_materno = self.cleaned_data['apellido_m']
        familiar.parentesco = self.cleaned_data['parentesco']

        
        if commit:
            familiar.save() 

        return familiar


class FamiliarEdicionForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombres', max_length=100)
    apellido_p = forms.CharField(label='Apellido paterno', max_length=100)
    apellido_m = forms.CharField(label='Apellido materno', max_length=100)
    parentesco = forms.CharField(label='Parentesco', max_length=50)
    # ELIMINADO: email
    password = forms.CharField(label='Nueva contraseña (opcional)', required=False, widget=forms.PasswordInput, max_length=10)
    
    class Meta:
        model = Familiar
        exclude = ['usuario', 'nombre', 'apellido_paterno', 'apellido_materno', 'parentesco', 'codFamiliar']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border-b-2 border-gray-300 focus:border-blue-500 px-2 py-2'
            })
        
        if self.instance:
            self.fields['first_name'].initial = self.instance.nombre
            self.fields['apellido_p'].initial = self.instance.apellido_paterno
            self.fields['apellido_m'].initial = self.instance.apellido_materno
            self.fields['parentesco'].initial = self.instance.parentesco


    def save(self, commit=True):
        familiar = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            familiar.usuario.password =password
            familiar.usuario.save()
        familiar.nombre = self.cleaned_data['first_name']
        familiar.apellido_paterno = self.cleaned_data['apellido_p']
        familiar.apellido_materno = self.cleaned_data['apellido_m']
        familiar.parentesco = self.cleaned_data['parentesco']


        if commit:
            familiar.save()

        return familiar
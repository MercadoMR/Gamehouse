
#Formularios para el jugador
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import models
from django.forms.fields import MultipleChoiceField
from .models import Usuario,Jugador,Genero,Plataforma,Juego,Opinion,JuegosFavoritos,Imagen,Compania,CDE,CPU
import datetime

class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username',
            'password1','password2']
        labels={
            'username':'Repita el NickName',
            'password1':'Contraseña',
            'password2':'Repita Contraseña'}
        widgets = {
        # telling Django your password field in the mode is a password input on the template
        'username':forms.TextInput(attrs={'class':'form-control'}),
        'password1': forms.PasswordInput(attrs={'class':'form-control'}) ,
        'password2': forms.PasswordInput(attrs={'class':'form-control'}) 
    }
        
#Valor para prueba: ♥
#Revisar https://stackoverflow.com/questions/46749405/formatting-data-from-a-datefield-using-modelform-django-1-11
#https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#timeinput
#https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#customizing-widget-instances
#https://docs.djangoproject.com/en/3.1/topics/forms/#looping-over-the-form-s-fields  
class UsuarioForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update(size='40')
        #self.fields['fec_nac'].widget.attrs.update({})
        #print("Campo:",self.fields['fec_nac'])
        #print("tipo:",type(self.fields['fec_nac']))
        #self.fields['fec_nac'].widget.attrs.update({'class': 'special'})
  def clean(self):
    super(UsuarioForm, self).clean()
    print(self.cleaned_data)
    campo_nombre = self.cleaned_data.get('nombre')
    campo_apellido = self.cleaned_data.get('apellido')
    if len(campo_nombre) < 3:
      self._errors['nombre'] = self.error_class(['Mínimo 3 caracteres'])
    if len(campo_apellido) < 3:
      self._errors['apellido'] = self.error_class(['Mínimo 3 caracteres'])
    return self.cleaned_data
  class Meta: #Esto solo se aplica a campos generados automaticamente
    model = Usuario
    fields = '__all__'
    #exclude
    #fields=['nombre','apellido','correo', 'fec_nac','contra']
    labels = {
            'nombre': 'Nombre de Usuario',
            'apellido': 'Tus apellidos',
            'correo': 'Introduce un correo electronico válido',
            'fec_nac': 'Introduce tu fecha de nacimiento'
    }
    help_texts = {
        'nombre': 'Cómo te llamas',
    }
    #https://stackoverflow.com/questions/37088697/showing-custom-error-messages-in-django-model-form-with-bootstrap
    #Change error_messages  to  error
    #https://docs.djangoproject.com/en/3.1/ref/models/fields/#error-messages
    error_messages = {
        'nombre': {
           'blank' : 'Esta en blanco',
           'invalid': 'No es valido',
        },
        'apellido': {
           'invalid': 'El apellido no es valido',
        },
        'correo': {
           'invalid': 'El correo introducido no es valido',
           'blank' : 'Correo en blanco'
        },
        'fec_nac': {
           'invalid': 'La fecha introducida no es valida',
        }
    }
    widgets = {
        # telling Django your password field in the mode is a password input on the template
        'nombre' :forms.TextInput(attrs={'class':'form-control'}),
        'apellido' :forms.TextInput(),
        'correo' :forms.EmailInput(), #Indica que se debe renderizar como email
        'fec_nac' :forms.DateInput(format='%d/%m/%Y',attrs={'placeholder': "Ejemplo.: dd/mm/aaaa"}) #FUnciona pero aun hay problema que no valida día
    }

"""
class UsuarioForm(forms.ModelForm):
  class Meta:
    model = Usuario
    fields = '__all__'
    #exclude
    #fields=['nombre','apellido','correo', 'fec_nac','contra']
    labels = {
            'nombre': 'Nombre de Usuario',
            'apellido': 'Tus apellidos',
            'correo': 'Introduce un correo electronico válido',
            'fec_nac': 'Introduce tu fecha de nacimiento',
    }
    help_texts = {
        'nombre': 'Texto de ayuda nombre.',
    }
    error_messages = {
        'nombre': {
           'max_length': "Este nombre es muy largo",
        },
    }
    widgets = {
        # telling Django your password field in the mode is a password input on the template
        'nombre':forms.TextInput(attrs={'class':'form-control'}),
        'apellidos':forms.TextInput(attrs={'class':'form-control'}),
        'correo':forms.TextInput(attrs={'class':'form-control'}),
        'fec_nac':forms.TextInput(attrs={'class':'form-control'}),
    }
"""
"""https://medium.com/@alfarhanzahedi/customizing-modelmultiplechoicefield-in-a-django-form-96e3ae7e1a07 
 generos = forms.ModelMultipleChoiceField(
                       widget = forms.CheckboxSelectMultiple,
                       queryset = Genero.objects.all()
               )"""
# customizing the ModelChoiceField made available in Django
# to have a better control at the data being displayed in the template(s)
class AdvancedModelChoiceIterator(models.ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj), self.field.label_from_instance(obj), obj)

class AdvancedModelChoiceField(models.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return AdvancedModelChoiceIterator(self)
    choices = property(_get_choices, MultipleChoiceField._set_choices)


class JugadorForm(forms.ModelForm):
  class Meta:
    model = Jugador
    fields = ['nickname','generos','plataformas']
    labels={
            'nickname':'Nickname',
    }

    # juegos = AdvancedModelChoiceField(
    #     queryset=Juego.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)

    generos = AdvancedModelChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    plataformas = AdvancedModelChoiceField(
        queryset=Plataforma.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    error_messages = {
        'nickname': {
           'max_length': "El id del jugador es de máximo 20 caracteres",
        },
    }

class MisGustosForm(forms.ModelForm):
  class Meta:
    model = Jugador
    fields = ['generos','plataformas']
    generos = AdvancedModelChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    plataformas = AdvancedModelChoiceField(
        queryset=Plataforma.objects.all(),
        widget=forms.CheckboxSelectMultiple)    



class GeneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields=['nombre']
        labels={
            'nombre':'Generos',
        }

class PlataformaForm(forms.ModelForm):
    class Meta:
        model= Plataforma
        fields=['nombre']
        labels={
            'nombre':'Plataformas',
        }

class CompaniaForm(forms.ModelForm):
    class Meta:
        model= Compania
        fields=['nombre']
        labels={'nombre':'Compañias'}

class ImagenForm(forms.ModelForm):
    class Meta:
        model=Imagen
        fields=['referencia']
        labels={'referencia':'URL de Imagen'}
        widgets = {
        'referencia':forms.TextInput(attrs={'class':'form-control'}),    
    }

class JuegoForm(forms.ModelForm):
    class Meta:
        model=Juego
        fields=['titulo','anio','descripcion','generos','plataformas','companias']
        labels={
                'titulo':'Título',
                'anio':'Año',
                'descripcion':'Descripción',
                # 'generos':'Generos',
                # 'plataformas':'Plataformas',
        }
        generos = AdvancedModelChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple)

        plataformas = AdvancedModelChoiceField(
        queryset=Plataforma.objects.all(),
        widget=forms.CheckboxSelectMultiple)

        companias = AdvancedModelChoiceField(
        queryset=Compania.objects.all(),
        widget=forms.CheckboxSelectMultiple)

        widgets = {
        # telling Django your password field in the mode is a password input on the template
        'titulo':forms.TextInput(attrs={'class':'form-control'}),
        'anio':forms.TextInput(attrs={'class':'form-control'}),
        'descripcion':forms.TextInput(attrs={'class':'form-control'}),
        #'referencia':forms.ImageField(),
        # 'generos':forms.TextInput(attrs={'class':'form-control'}),
        # 'plataformas':forms.TextInput(attrs={'class':'form-control'}),
    }    

class OpinionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gusto'].widget.attrs.update({'class': 'star'})
        self.fields['guion'].widget.attrs.update({'class': 'star'})
        self.fields['artes'].widget.attrs.update({'class': 'star'})
        self.fields['jugabilidad'].widget.attrs.update({'class': 'star'})
        self.fields['tecnico'].widget.attrs.update({'class': 'star'})
        
    gusto = forms.TypedChoiceField(choices=Opinion.CHOICES, widget=forms.RadioSelect, coerce=int)
    guion = forms.TypedChoiceField(choices=Opinion.CHOICES, widget=forms.RadioSelect, coerce=int)
    artes = forms.TypedChoiceField(choices=Opinion.CHOICES, widget=forms.RadioSelect, coerce=int)
    jugabilidad = forms.TypedChoiceField(choices=Opinion.CHOICES, widget=forms.RadioSelect, coerce=int)
    tecnico = forms.TypedChoiceField(choices=Opinion.CHOICES, widget=forms.RadioSelect, coerce=int)
    class Meta:
        model = Opinion
        exclude = ['jugador','juego','comentario','puntaje_total']
        labels={
            'gusto':'¿Qué tanto te gustó el juego en general?',
            'guion':'Calificación del guión del juego',
            'artes':'Calificación de la arte del juego',
            'jugabilidad':'Calificación de la jugabilidad del juego',
            'tecnico':'Calificación del aspecto técnico del juego',
        }
        """
        labels={
                'comentario':'Introduce tu impresión en general de este juego',
        }
        
        widgets = {
        'gusto': forms.TypedChoiceField(),
        #'guion': forms.RadioSelect(choices = Opinion.CHOICES),
        #'artes': forms.RadioSelect(),
        #'jugabilidad': forms.RadioSelect(),
        #'tecnico': forms.RadioSelect(),
        }
        """
        
        

class JuegosFavoritosForm(forms.ModelForm):
    class Meta:
        model=JuegosFavoritos
        fields=['jugador', 'juego']

class CdeForm(forms.ModelForm):
    class Meta:
        model=CDE
        exclude=['jugador']
        labels={'cde0':'Caracteristica 1',
        'cde1':'Caracteristica 2',
        'cde2':'Caracteristica 3',
        'cde3':'Caracteristica 4',
        'cde4':'Caracteristica 5',
        'cde5':'Caracteristica 6',
        'cde6':'Caracteristica 7',
        'cde7':'Caracteristica 8',
        'cde8':'Caracteristica 9',
        'cde9':'Caracteristica 10'
        }
        

class CpuForm(forms.ModelForm):
    class Meta:
        model=CPU
        exclude=['jugador']
        labels={'cpu0':'Caracteristica 1',
        'cpu1':'Caracteristica 2',
        'cpu2':'Caracteristica 3',
        'cpu3':'Caracteristica 4',
        'cpu4':'Caracteristica 5',
        'cpu5':'Caracteristica 6',
        'cpu6':'Caracteristica 7',
        'cpu7':'Caracteristica 8',
        'cpu8':'Caracteristica 9',
        'cpu9':'Caracteristica 10',
        }

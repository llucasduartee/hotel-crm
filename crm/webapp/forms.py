from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reservation, Room

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput



class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']




class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



class CreateReservationForm(forms.ModelForm):
    number_of_people = forms.IntegerField(min_value=1, max_value=6)
    check_in = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))
    check_out = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'}))
    class Meta:

        model = Reservation
        fields = ['first_name', 'last_name', 'email','check_in', 'check_out']
    def __init__(self, *args, **kwargs):
        super(CreateReservationForm, self).__init__(*args, **kwargs)

        
        self.fields['number_of_people'].widget.attrs.update({'class': 'form-control'})



class UpdateReservationForm(forms.ModelForm):

    class Meta:

        model = Reservation
        fields = ['first_name', 'last_name', 'email', 'check_in', 'check_out']


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'capacity']

class UpdateRoomForm(forms.ModelForm):
    capacity = forms.IntegerField(min_value=1, max_value=6)
    class Meta:
        model = Room
        fields = ['number', 'capacity']
        def __init__(self, *args, **kwargs):
            super(CreateReservationForm, self).__init__(*args, **kwargs)

        
            self.fields['capacity'].widget.attrs.update({'class': 'form-control'})
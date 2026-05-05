from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User 

class RegisterForm(UserCreationForm): 
    first_name = forms.CharField(max_length = 150, required = True)
    last_name = forms.CharField(max_length = 150, required = True)
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit = True): 
        user = super().save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit: 
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 150)
    last_name = forms.CharField(max_length = 150)
    email = forms.EmailField()

    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for field in self.fields.values(): 
            field.widget.attrs['class'] = 'form-control'
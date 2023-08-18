from django import forms
from django.contrib.auth import authenticate

from .models import CustomUser


class SignUpForm(forms.ModelForm):
	password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
	password2 = forms.CharField(label = 'Password confirmation', widget = forms.PasswordInput)
	photo = forms.ImageField(required = False, widget = forms.FileInput)
	
	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'username']
		widgets = {
			'first_name': forms.TextInput(attrs = {'class': 'form-control'}),
			'last_name': forms.TextInput(attrs = {'class': 'form-control'}),
			'username': forms.TextInput(attrs = {'class': 'form-control'}),
			'password1': forms.PasswordInput(attrs = {'class': 'form-control'}),
			'password2': forms.PasswordInput(attrs = {'class': 'form-control'}),
			'photo': forms.FileInput(attrs = {'class': 'form-control-file'}),
		}
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2
	
	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class SignInForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")

        return cleaned_data
from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    email = forms.EmailField(label="E-mail")
    username = forms.CharField(label="Username")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords are not equal")
        
        values = {
            "first_name" : first_name,
            "last_name" : last_name,
            "email" : email,
            "username" : username,
            "password1" : password1,
        }

        return values

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


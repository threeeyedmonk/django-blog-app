from django import forms
from django.contrib.auth.models import User
from blog.models import Post

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def check_confirm_password(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')
        if not (pwd1 and pwd2):
            raise forms.ValidationError("You must confirm your password.")
        elif pwd1 != pwd2:
            raise forms.ValidationError("Passwords do not match.")
        return pwd1

class CreatePostForm(forms.ModelForm):
    post_title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    post_text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
        }
    ))
    class Meta():
        model = Post
        fields = ['post_title', 'post_text']

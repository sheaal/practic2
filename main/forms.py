from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from unicodedata import category

from .models import AdvUser, Applic, Category
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import Applic, AdditionalImage
from django.forms import inlineformset_factory

# class ChangeUserInfoForm(forms.ModelForm):
#    email = forms.EmailField(required=True,
#                             label='Адрес электронной почты')
#
#    class Meta:
#        model = AdvUser
#        fields = ('username', 'email', 'first_name', 'last_name',
#                  'send_messages')


# class RegisterUserForm(forms.ModelForm):
#    email = forms.EmailField(required=True, label='Адрес электронной почты')
#    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)
#    username = forms.CharField(label='Имя пользователя')
#    sur_name = forms.CharField(label='Фамилия', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
#    n_name = forms.CharField(label='Имя', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
#    pat_mic = forms.CharField(label='Отчество', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
#
#    class Meta:
#        model = AdvUser
#        fields = ('sur_name', 'n_name', 'pat_mic', 'username', 'email', 'password1', 'password2', 'send_messages')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)

    sur_name = forms.CharField(label='Фамилия', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    n_name = forms.CharField(label='Имя', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    pat_mic = forms.CharField(label='Отчество', max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = AdvUser
        fields = ('sur_name', 'n_name', 'pat_mic', 'username', 'email', 'password1', 'password2', 'send_messages')


    def clean_password1(self):
           password1 = self.cleaned_data['password1']
           if password1:
               password_validation.validate_password(password1)
           return password1


    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                 'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        return user

    # def clean_last_name(self):
    #     sur_name = self.cleaned_data['sur_name']
    #     if not sur_name.isalpha():
    #         raise forms.ValidationError("В фамилии не должны присутствовать цифры")
    #     return sur_name
    #
    # def clean_name(self):
    #     n_name = self.cleaned_data['n_name']
    #     if not n_name.isalpha():
    #         raise forms.ValidationError("В имени не должны присутствовать цифры")
    #     return n_name
    #
    # def clean_patronymic(self):
    #     pat_mic = self.cleaned_data['pat_mic']
    #     if not pat_mic.isalpha():
    #         raise forms.ValidationError("В отчестве не должны присутствовать цифры")
    #     return pat_mic
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if AdvUser.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Пользователь с таким email уже существует")
    #     return email

class ApplicForm(forms.ModelForm):
    class Meta:
       model = Applic
       fields = ['title', 'content', 'category', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Изображение превышает 2 Мб")
        return image


AIFormSet = inlineformset_factory(Applic, AdditionalImage, fields='__all__')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CategoryForm(forms.ModelForm):
   class Meta:
       model = Category
       fields = ['category_title']


class RequestStatusCompleted(forms.ModelForm):
    class Meta:
        model = Applic
        fields = ['image_design']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Изображение превышает 2 Мб")
        return image

class RequestStatusAcceptWork(forms.ModelForm):
    class Meta:
        model = Applic
        fields = ['comment']
from django import forms
from .models import Recipe, Ingredient, RecipeIngredients
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите название рецепта'
        })
        self.fields['name'].label = 'Название рецепта' 


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'measuring', 'cost']


class ReceiptIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'measure', 'measure_weight']


class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['measure', 'measure_weight']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Данные не указаны'
        })
        
        self.fields['email'].label = 'Электронная почта'
        self.fields['email'].widget.attrs.update({
            'required': True,
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите вашу электронную почту'
        })
        
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите пароль'
        })
        
        self.fields['password_confirm'].label = 'Подтвердите пароль'
        self.fields['password_confirm'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Повторите пароль'
        })

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return password_confirm


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Данные не указаны'
        })
        
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите пароль'
        })


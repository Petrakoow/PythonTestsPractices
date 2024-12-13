from django import forms
from .models import Recipe, Ingredient, RecipeIngredient, Unit
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title']  

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите название рецепта'
        })
        self.fields['title'].label = 'Название рецепта'


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['title', 'raw_weight', 'cooked_weight', 'cost', 'unit']

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите название ингредиента'
        })
        self.fields['title'].label = 'Название ингредиента'
        self.fields['raw_weight'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите сырой вес'
        })
        self.fields['cooked_weight'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите вес после готовки'
        })
        self.fields['cost'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите стоимость'
        })

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data



class RecipeIngredientForm(forms.ModelForm):  
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient']  

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].empty_label = 'Выберите ингредиент или оставьте пустым'
        self.fields['ingredient'].required = False
        self.fields['ingredient'].widget.attrs.update({
            'class': 'form-control rounded-pill',
        })


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
            raise forms.ValidationError("Два пароля не совпадают")
        return password_confirm
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username


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

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'conversion_to_grams']

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите название единицы измерения'
        })
        self.fields['name'].label = 'Название единицы измерения'

        self.fields['conversion_to_grams'].widget.attrs.update({
            'class': 'form-control rounded-pill',
            'placeholder': 'Введите коэффициент конверсии в граммы'
        })
        self.fields['conversion_to_grams'].label = 'Коэффициент конверсии'
    
    def clean_conversion_to_grams(self):
        conversion = self.cleaned_data.get('conversion_to_grams')
        if conversion <= 0:
            raise forms.ValidationError("Коэффициент должен быть больше 0.")
        return conversion


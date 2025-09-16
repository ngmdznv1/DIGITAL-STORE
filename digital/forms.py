from django import forms

from .models import Category, ShippingAddress, Region, City, Profile
from django_svg_image_form_field import SvgAndImageFormField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'E-mail'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'E-mail'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Ваша фамилия'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class ShippingForm(forms.ModelForm):
    # address = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Адрес (ул, дом, кв)'
    # }))
    #
    # phone = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Номер телефона'
    # }))
    #
    # region = forms.CharField(widget=forms.Select(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Регион'
    # }))
    #
    # city = forms.CharField(widget=forms.Select(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Город'
    # }))
    #
    # comment = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Комментарий к заказу'
    # }))
    #
    # first_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Ваше имя...'
    # }))
    #
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Ваша фамилия...'
    # }))
    #
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'class': 'contact__section-input',
    #     'placeholder': 'Ваша почта'
    # }))
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Выберите регион",
        widget=forms.Select(attrs={'class': 'contact__section-input'}),
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город",
        widget=forms.Select(attrs={'class': 'contact__section-input'}),
    )

    class Meta:
        model = ShippingAddress
        fields = ('address', 'phone', 'region', 'city', 'comment', 'first_name', 'last_name', 'email')
        widgets = {
            'address': forms.TextInput(attrs={'class': 'contact__section-input', 'placeholder': 'Адрес (ул, дом, кв)'}),
            'phone': forms.TextInput(attrs={'class': 'contact__section-input', 'placeholder': 'Номер телефона'}),
            'comment': forms.Textarea(attrs={'class': 'contact__section-input', 'placeholder': 'Комментарий к заказу'}),
            'first_name': forms.TextInput(attrs={'class': 'contact__section-input', 'placeholder': 'Имя...'}),
            'last_name': forms.TextInput(attrs={'class': 'contact__section-input', 'placeholder': 'Фамилия...'}),
            'email': forms.EmailInput(attrs={'class': 'contact__section-input', 'placeholder': 'Почта'}),
        }


class EditAccountForm(UserChangeForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'contact__section-input'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    street = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    house = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    flat = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
    }))

    class Meta:
        model = Profile
        fields = ('phone', 'city', 'street', 'house', 'flat')
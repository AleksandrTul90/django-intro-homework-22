from django import forms
from django.core.files.uploadedfile import UploadedFile

from catalog.constants import FORBIDDEN_WORDS
from catalog.models import Product

MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = ('image/jpeg', 'image/png')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите название товара'},
        )
        self.fields['description'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите описание товара',
            },
        )
        self.fields['image'].widget = forms.ClearableFileInput(
            attrs={'class': 'form-control'},
        )
        self.fields['category'].widget = forms.Select(attrs={'class': 'form-select'})
        self.fields['price'].widget = forms.NumberInput(
            attrs={'class': 'form-control', 'step': '0.01', 'min': '0'},
        )

        self.fields['image'].required = False

    def _validate_forbidden_words(self, value, field_label):
        if not value:
            return value

        lower_value = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lower_value:
                raise forms.ValidationError(
                    f'В поле «{field_label}» нельзя использовать запрещённое слово «{word}».'
                )
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return self._validate_forbidden_words(name, 'наименование')

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return self._validate_forbidden_words(description, 'описание')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена продукта не может быть отрицательной. Укажите корректное значение.'
            )
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image or not isinstance(image, UploadedFile):
            return image

        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError(
                'Загружайте изображение в формате JPEG или PNG.'
            )

        if image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError(
                'Размер изображения не должен превышать 5 МБ.'
            )

        return image

from .models import KksCodeModel
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, Select, ChoiceField, Form, PasswordInput, \
    CharField, ModelChoiceField, modelformset_factory, ModelMultipleChoiceField, MultipleChoiceField, SelectMultiple, \
    FileField, ClearableFileInput, FileInput, DateTimeField, DateTimeInput

class KksCodeForm(ModelForm):
    class Meta:
        model = KksCodeModel
        fields = '__all__'
        exclude = [
            'add_date',
            'text',
            'status',
            'author',
            'index_number',
            'sector5',
            'sector6'
        ]
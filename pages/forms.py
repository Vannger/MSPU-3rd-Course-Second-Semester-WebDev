from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spell, Tag, Comment


class SpellForm(forms.ModelForm):
    class Meta:
        model = Spell
        fields = ['name', 'spell_lvl', 'desc', 'add_date', 'image', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'tome-input form-control',
                'placeholder': 'e.g. Fireball',
            }),
            'spell_lvl': forms.NumberInput(attrs={
                'class': 'tome-input form-control',
                'min': 0,
                'max': 9,
                'placeholder': '0 = Cantrip, 1–9 = Spell level',
            }),
            'desc': forms.Textarea(attrs={
                'class': 'tome-input tome-textarea form-control',
                'rows': 5,
                'placeholder': "Describe the spell's effects…",
            }),
            'add_date': forms.DateInput(attrs={
                'class': 'tome-input form-control',
                'type': 'date',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'tome-input form-control',
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'tome-tags-checklist',
            }),
        }
        labels = {
            'name':      'Spell Name',
            'spell_lvl': 'Spell Level',
            'desc':      'Description',
            'add_date':  'Date Added',
            'image':     'Spell Image (optional)',
            'tags':      'Tags',
        }


class RegisterForm(UserCreationForm):
    """Simple registration form — just username + password."""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'tome-input form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Choose a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your password'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class FeedbackForm(forms.Form):
    subject = forms.CharField(
        label='Тема письма',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'О чем вы хотите спросить?'})
    )
    email = forms.EmailField(
        label='Ваш Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    text = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишите ваше сообщение здесь...'})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment…',
            }),
        }
        labels = {
            'text': 'Comment',
        }

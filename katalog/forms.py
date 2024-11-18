from django import forms
from .models import BookModel

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ['pdf_file', 'title', 'description', 'author', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book description'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter genre book'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

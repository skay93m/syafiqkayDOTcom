from django import forms
from .models import Reference

class ReferenceForm(forms.ModelForm):
    category = forms.CharField(
        max_length=100,
        required=False,
        help_text="Separate multiple categories with commas (e.g., web-development, django, python)",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., web-development, django, python',
            'class': 'form-control',
            'data-toggle': 'tooltip',
            'title': 'Common categories: web-development, mobile-development, data-science, research, tutorial, security, performance'
        })
    )
    
    class Meta:
        model = Reference
        fields = ['title', 'summary', 'content', 'url', 'category', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_category(self):
        category = self.cleaned_data.get('category', '')
        if category:
            # Clean up categories: remove extra spaces, convert to lowercase
            categories = [cat.strip().lower() for cat in category.split(',')]
            # Remove empty categories
            categories = [cat for cat in categories if cat]
            # Join back with consistent formatting
            return ', '.join(categories)
        return category

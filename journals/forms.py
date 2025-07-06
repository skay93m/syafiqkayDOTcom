from django import forms
from .models import Journal

class JournalForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=200,
        required=False,
        help_text="Separate multiple tags with commas (e.g., personal, reflection, development)",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., personal, reflection, development, thoughts',
            'class': 'form-control',
            'data-toggle': 'tooltip',
            'title': 'Common tags: personal, reflection, development, thoughts, tutorial, learning, work, travel, goals'
        })
    )
    
    class Meta:
        model = Journal
        fields = ['title', 'summary', 'content', 'tags', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Clean up tags: remove extra spaces, convert to lowercase
            tag_list = [tag.strip().lower() for tag in tags.split(',')]
            # Remove empty tags
            tag_list = [tag for tag in tag_list if tag]
            # Join back with consistent formatting
            return ', '.join(tag_list)
        return tags

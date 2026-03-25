from django import forms
from .models import Word, Definition, Category, Comment

class WordForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Word
        fields = ['term', 'categories']
        widgets = {
            'term': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class WordEditForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Word
        fields = ['categories']

class DefinitionForm(forms.ModelForm):
    class Meta:
        model = Definition
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': ''} # Hides the default 'Body' label
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, 
                'placeholder': 'Join the discussion... leave a comment!'
            }),
        }
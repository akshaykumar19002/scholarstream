from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1-5 rating

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = Review
        fields = ['comment', 'rating', 'anonymous']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Comment too short")
        return comment

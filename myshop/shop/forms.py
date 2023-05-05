from django import forms
from .models import Comment


class UserRegistrationForm(forms.ModelForm):
    advantages = forms.CharField(
        widget=forms.Textarea(
            attrs={"cols": "60", "rows": "1", "placeholder": "Достоинства"}
        ),
        required=False,
    )

    disadvantages = forms.CharField(
        widget=forms.Textarea(
            attrs={"cols": "60", "rows": "1", "placeholder": "Недостатки"}
        ),
        required=False,
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={"cols": "60", "rows": "1", "placeholder": "Комментарий"}
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_score"].widget.attrs.update({"min": "0", "max": "5"})

    class Meta:
        model = Comment
        fields = ["product_score"]
        labels = {
            "product_score": "Оцените покупку",
        }

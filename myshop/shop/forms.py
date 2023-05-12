from django import forms
from .models import Comment, CommentImage


class ReviewForm(forms.ModelForm):
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


class CommentImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs.update(
            {"class": "form-control form-control-sm"}
        )

    class Meta:
        model = CommentImage
        fields = ["image"]


CommentImageFormSet = forms.formset_factory(CommentImageForm, extra=3)

from django import forms
from .models import Book, Member, Transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

class IssueForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.filter(stock__gt=0),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned = super().clean()
        member = cleaned.get("member")
        if member and member.debt > 500:
            raise ValidationError("Member owes more than ₹500.")
        return cleaned


class ReturnForm(forms.Form):
    transaction = forms.ModelChoiceField(
        queryset=Transaction.objects.filter(return_date__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    days_late = forms.IntegerField(
        min_value=0,
        initial=0,
        help_text="Number of days late",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def save(self):
        tx = self.cleaned_data["transaction"]
        days = self.cleaned_data["days_late"]
        fee_per_day = 5
        fee = days * fee_per_day

        tx.return_date = timezone.now()
        tx.fee = fee
        tx.save()

        book = tx.book
        book.stock += 1
        book.save()

        member = tx.member
        member.debt += fee
        member.save()
        return tx

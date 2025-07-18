from django.db import models
from django.utils import timezone

class Book(models.Model):
    title      = models.CharField(max_length=200)
    author     = models.CharField(max_length=200)
    isbn       = models.CharField(max_length=20, unique=True)
    publisher  = models.CharField(max_length=200, blank=True)
    stock      = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.stock})"


class Member(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    debt  = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} – ₹{self.debt}"


class Transaction(models.Model):
    book         = models.ForeignKey(Book, on_delete=models.CASCADE)
    member       = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date   = models.DateField(default=timezone.now)
    return_date  = models.DateField(null=True, blank=True)
    fee          = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.book} → {self.member}"

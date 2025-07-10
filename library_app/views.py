from django.shortcuts import render, redirect
from .forms import IssueForm, ReturnForm
import requests
from django.contrib import messages
from django.conf import settings
from .models import Book, Member, Transaction  

def dashboard(request):
    return render(request, "dashboard.html", {
        "book_count": Book.objects.count(),
        "tx_open": Transaction.objects.filter(return_date__isnull=True).count(),
    })

from django.db.models import Q

def issue_book(request):
    book_search = request.GET.get('book_search', '')
    member_search = request.GET.get('member_search', '')

    books = Book.objects.filter(stock__gt=0)
    members = Member.objects.all()

    if book_search:
        books = books.filter(Q(title__icontains=book_search) | Q(author__icontains=book_search))

    if member_search:
        members = members.filter(Q(name__icontains=member_search) | Q(email__icontains=member_search))

    if request.method == 'POST':
        form = IssueForm(request.POST)
        form.fields['book'].queryset = books
        form.fields['member'].queryset = members
        if form.is_valid():
            book = form.cleaned_data['book']
            member = form.cleaned_data['member']

            # Create the transaction
            tx = Transaction.objects.create(book=book, member=member)

            # Decrease stock
            book.stock -= 1
            book.save()
            messages.success(request, f"'{book.title}' issued to {member.name}.")

            return redirect('dashboard')

    else:
        form = IssueForm()
        form.fields['book'].queryset = books
        form.fields['member'].queryset = members

    return render(request, 'issue.html', {'form': form, 'book_search': book_search, 'member_search': member_search})

def return_book(request):
    tx_search = request.GET.get('tx_search', '')
    transactions = Transaction.objects.filter(return_date__isnull=True)

    if tx_search:
        transactions = transactions.filter(
            Q(book__title__icontains=tx_search) |
            Q(member__name__icontains=tx_search)
        )

    if request.method == 'POST':
        form = ReturnForm(request.POST)
        form.fields['transaction'].queryset = transactions
        if form.is_valid():
            tx = form.save()
            messages.success(request, f"'{tx.book.title}' returned by {tx.member.name}. Fee: ₹{tx.fee}")
            return redirect('dashboard')
    else:
        form = ReturnForm()
        form.fields['transaction'].queryset = transactions

    return render(request, 'return.html', {'form': form, 'tx_search': tx_search})


# library_app/views.py
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book


def import_books(request):
    """
    Import N books from the Frappe Library API.

    The user supplies:
      • title  (string to search in book titles)
      • quantity (how many NEW books they want)

    We keep calling the API, page‑by‑page (20 books each),
    until either:
      • we have inserted `quantity` unique books, OR
      • the API runs out of results.
    """
    if request.method == "POST":
        title      = request.POST.get("title", "").strip()
        quantity   = int(request.POST.get("quantity", 0))

        imported   = 0      # new records saved
        total_seen = 0      # all records processed (for UX)
        page       = 1

        while imported < quantity:
            resp = requests.get(
                "https://frappe.io/api/method/frappe-library",
                params={"page": page, "title": title}
            )
            data = resp.json().get("message", [])

            if not data:         # no more pages
                break

            for b in data:
                if imported >= quantity:
                    break
                total_seen += 1

                isbn = b["isbn"] or b["isbn13"]
                if not isbn:
                    continue          # skip if ISBN missing

                _, created = Book.objects.get_or_create(
                    isbn=isbn,
                    defaults={
                        "title":     b["title"],
                        "author":    b["authors"],
                        "publisher": (b["publisher"] or "")[:200],
                        "stock":     1,
                    },
                )
                if created:
                    imported += 1

            page += 1     # fetch next 20 books

        duplicates = total_seen - imported
        messages.success(
            request,
            f"Imported {imported} new book(s). {duplicates} duplicate(s) skipped."
        )

    return render(request, "import.html")


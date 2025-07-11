from django.contrib import admin
from .models import Book, Member, Transaction

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "stock")
    search_fields = ("title", "author", "isbn")

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "debt")
    search_fields = ("name", "email")

admin.site.register(Transaction)

admin.site.site_header = "📚 Library Management Admin"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Manage Books, Members & Transactions"
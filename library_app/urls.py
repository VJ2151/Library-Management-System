from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("issue/", views.issue_book, name="issue_book"),
    path("return/", views.return_book, name="return_book"),
    path("import/", views.import_books, name="import_books"),
    path("transactions/", views.all_transactions, name="all_transactions"),

]

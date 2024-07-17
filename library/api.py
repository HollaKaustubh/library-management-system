from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Book, Borrow
from .schemas import BookSchema, BorrowSchema, ErrorSchema
from django.db.models import Q
from datetime import datetime
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)

@api.get("/books", response=list[BookSchema])
def list_books(request):
    return Book.objects.all()

@api.get("/books/{book_id}", response=BookSchema)
def get_book(request, book_id: int):
    return get_object_or_404(Book, id=book_id)

@api.post("/books", response={201: BookSchema, 400: ErrorSchema})
def create_book(request, book: BookSchema):
    try:
        return 201, Book.objects.create(**book.dict())
    except Exception as e:
        return 400, {"message": str(e)}

@api.put("/books/{book_id}", response={200: BookSchema, 400: ErrorSchema})
def update_book(request, book_id: int, data: BookSchema):
    book = get_object_or_404(Book, id=book_id)
    for attr, value in data.dict().items():
        setattr(book, attr, value)
    try:
        book.save()
        return 200, book
    except Exception as e:
        return 400, {"message": str(e)}

@api.delete("/books/{book_id}", response={204: None, 404: ErrorSchema})
def delete_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return 204, None

@api.get("/available-books", response=list[BookSchema])
def list_available_books(request):
    return Book.objects.filter(quantity__gt=0)

@api.post("/borrow", response={201: BorrowSchema, 400: ErrorSchema})
def borrow_book(request, borrow: BorrowSchema):
    user = get_object_or_404(User, id=borrow.user_id)
    book = get_object_or_404(Book, id=borrow.book_id)

    if book.quantity <= 0:
        return 400, {"message": "Book is not available for borrowing"}

    if Borrow.objects.filter(Q(user=user) & Q(book=book) & Q(return_date__isnull=True)).exists():
        return 400, {"message": "You have already borrowed this book"}

    book.quantity -= 1
    book.save()

    borrow_record = Borrow.objects.create(user=user, book=book)
    return 201, borrow_record

@api.post("/return", response={200: BorrowSchema, 400: ErrorSchema})
def return_book(request, borrow_id: int):
    borrow_record = get_object_or_404(Borrow, id=borrow_id)

    if borrow_record.return_date:
        return 400, {"message": "This book has already been returned"}

    borrow_record.return_date = datetime.now()
    borrow_record.save()

    book = borrow_record.book
    book.quantity += 1
    book.save()

    return 200, borrow_record
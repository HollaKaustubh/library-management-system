from ninja import Schema
from datetime import datetime

class BookSchema(Schema):
    id: int = None
    title: str
    author: str
    isbn: str
    quantity: int

class BorrowSchema(Schema):
    id: int = None
    user_id: int
    book_id: int
    borrow_date: datetime = None
    return_date: datetime = None

class ErrorSchema(Schema):
    message: str
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Borrow
from django.urls import reverse
from ninja.testing import TestClient
from .api import api

class LibraryAPITestCase(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(title='Test Book', author='Test Author', isbn='1234567890', quantity=5)

    def test_list_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_book(self):
        data = {'title': 'New Book', 'author': 'New Author', 'isbn': '0987654321', 'quantity': 3}
        response = self.client.post("/books", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_borrow_book(self):
        data = {'user_id': self.user.id, 'book_id': self.book.id}
        response = self.client.post("/borrow", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Borrow.objects.count(), 1)

    def test_return_book(self):
        borrow = Borrow.objects.create(user=self.user, book=self.book)
        response = self.client.post(f"/return?borrow_id={borrow.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Borrow.objects.get(id=borrow.id).return_date)    
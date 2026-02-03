from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Book, Author


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Includes tests for CRUD, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create a test client
        self.client = APIClient()

        # Create a user for authenticated requests
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create an author and books for testing
        self.author = Author.objects.create(name="Chinua Achebe")

        self.book1 = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author
        )

        self.book2 = Book.objects.create(
            title="No Longer at Ease",
            publication_year=1960,
            author=self.author
        )

        # URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.id})
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", kwargs={"pk": self.book1.id})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book1.id})

    # ----------------------------------------------------
    # LIST VIEW TEST
    # ----------------------------------------------------
    def test_get_book_list(self):
        """Test retrieving the list of books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ----------------------------------------------------
    # DETAIL VIEW TEST
    # ----------------------------------------------------
    def test_get_book_detail(self):
        """Test retrieving a single book."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # ----------------------------------------------------
    # CREATE VIEW - REQUIRES AUTHENTICATION
    # ----------------------------------------------------
    def test_create_book_requires_auth(self):
        """Ensure user must be authenticated to create a book."""
        data = {
            "title": "New Book",
            "publication_year": 2001,
            "author": self.author.id
        }
        # Attempt without login
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Now login and retry
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ----------------------------------------------------
    # UPDATE VIEW - REQUIRES AUTHENTICATION
    # ----------------------------------------------------
    def test_update_book(self):
        """Ensure authenticated users can update a book."""
        self.client.login(username="testuser", password="password123")

        data = {"title": "Updated Title", "publication_year": 1959, "author": self.author.id}
        response = self.client.put(self.update_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ----------------------------------------------------
    # DELETE VIEW - REQUIRES AUTHENTICATION
    # ----------------------------------------------------
    def test_delete_book(self):
        """Ensure authenticated users can delete a book."""
        self.client.login(username="testuser", password="password123")

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ----------------------------------------------------
    # FILTERING TESTS
    # ----------------------------------------------------
    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.list_url, {"publication_year": 1958})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {"title": "Things Fall Apart"})
        self.assertEqual(len(response.data), 1)

    # ----------------------------------------------------
    # SEARCH TESTS
    # ----------------------------------------------------
    def test_search_books(self):
        response = self.client.get(self.list_url, {"search": "Achebe"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ----------------------------------------------------
    # ORDERING TESTS
    # ----------------------------------------------------
    def test_order_books_by_title(self):
        response = self.client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    # ----------------------------------------------------
    # PERMISSION TESTS
    # ----------------------------------------------------
    def test_unauthenticated_user_cannot_create_book(self):
        data = {"title": "Blocked Book", "publication_year": 2022, "author": self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

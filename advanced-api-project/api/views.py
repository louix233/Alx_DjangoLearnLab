from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework


from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer



# ------------------------------------------------------
# BOOK LIST VIEW — WITH FILTERING, SEARCHING, ORDERING
# ------------------------------------------------------
# This view now allows API users to:
# - Filter books by title, author, and publication_year
# - Search text within title and author name
# - Order results by any field (title, publication_year, etc.)
# ------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable DRF filtering features
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # --- FILTERING SETUP ---
    # Allows: ?title=abc  ?publication_year=2020  ?author=3
    filterset_fields = ['title', 'publication_year', 'author']

    # --- SEARCH SETUP ---
    # Searching works with: ?search=keyword
    search_fields = ['title', 'author__name']

    # --- ORDERING SETUP ---
    # Allows: ?ordering=title  OR  ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']  # default ordering


# OTHER CRUD VIEWS (unchanged, kept as reference)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

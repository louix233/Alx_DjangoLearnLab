from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter


from django_filters import rest_framework

from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


# ------------------------------------------------------
# BOOK LIST VIEW — WITH FILTERING, SEARCHING, ORDERING
# ------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # DRF filter backends — Must include filters.OrderingFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,       
        filters.OrderingFilter,     
    ]

    # Filtering fields: ?title=.. ?publication_year=.. ?author=..
    filterset_fields = ['title', 'publication_year', 'author']

    # Search: ?search=keyword
    search_fields = ['title', 'author__name']

    # Ordering: ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']  # default ordering


# ------------------------------------------------------
# BOOK DETAIL VIEW — Retrieve single book
# ------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ------------------------------------------------------
# BOOK CREATE VIEW — Authenticated users only
# ------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic can go here
        serializer.save()


# ------------------------------------------------------
# BOOK UPDATE VIEW — Authenticated users only
# ------------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Custom logic such as logging or validation
        serializer.save()


# ------------------------------------------------------
# BOOK DELETE VIEW — Authenticated users only
# ------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

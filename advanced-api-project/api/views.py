from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer



# ------------------------------------------------------
# BOOK LIST VIEW
# Retrieves ALL books (Read-only, available to everyone)
# ------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


# ------------------------------------------------------
# BOOK DETAIL VIEW
# Retrieves a single book by PK (Read-only)
# ------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


# ------------------------------------------------------
# BOOK CREATE VIEW
# Creates a new Book entry (Authenticated users only)
# Custom validation and save logic included
# ------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users

    # Custom behavior: add extra validation or logging
    def perform_create(self, serializer):
        # You can add extra logic here such as attaching request.user
        # Example: serializer.save(owner=self.request.user)
        serializer.save()


# ------------------------------------------------------
# BOOK UPDATE VIEW
# Updates an existing Book (Authenticated users only)
# Custom logic included for updates
# ------------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users

    # Custom behavior on update
    def perform_update(self, serializer):
        # Add hooks such as logging or additional validation
        serializer.save()


# ------------------------------------------------------
# BOOK DELETE VIEW
# Deletes a Book (Authenticated users only)
# ------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users


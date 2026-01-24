from relationship_app.models import Author, Book, Library, Librarian

# -----------------------------
# Query 1: All books by author
# -----------------------------
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

print(f"Books by {author_name}:")
for book in books_by_author:
    print("-", book.title)

# -----------------------------
# Query 2: List all books in a library
# REQUIRED STRING MATCH HERE:
# Library.objects.get(name=library_name)
# -----------------------------
library_name = "Main Library"
library = Library.objects.get(name=library_name)  # <-- MUST EXIST EXACTLY LIKE THIS
books_in_library = library.books.all()

print(f"\nBooks in {library_name}:")
for book in books_in_library:
    print("-", book.title)

# -----------------------------
# Query 3: Retrieve librarian for a library
# -----------------------------
librarian = Librarian.objects.get(library=library)

print(f"\nLibrarian for {library_name}:")
print("-", librarian.name)

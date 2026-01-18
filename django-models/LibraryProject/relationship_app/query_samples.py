"""
Run this script from the project root (where manage.py is) with:

python manage.py shell < relationship_app/query_samples.py

This script demonstrates:
1) Query all books by a specific author (ForeignKey)
2) List all books in a library (ManyToMany)
3) Retrieve the librarian for a library (OneToOne)
"""

from relationship_app.models import Author, Book, Library, Librarian

# ----------------------------
# Optional: sample data setup
# ----------------------------
# You can delete this block if your checker expects only queries.
author, _ = Author.objects.get_or_create(name="Chinua Achebe")

book1, _ = Book.objects.get_or_create(title="Things Fall Apart", author=author)
book2, _ = Book.objects.get_or_create(title="No Longer at Ease", author=author)

library, _ = Library.objects.get_or_create(name="Main Library")
library.books.add(book1, book2)

librarian, _ = Librarian.objects.get_or_create(name="Alice Johnson", library=library)

# -----------------------------------------
# 1) Query all books by a specific author
# -----------------------------------------
specific_author = Author.objects.get(name="Chinua Achebe")
books_by_author = Book.objects.filter(author=specific_author)

print("Books by author:", specific_author.name)
for b in books_by_author:
    print("-", b.title)

# -----------------------------------------
# 2) List all books in a library
# -----------------------------------------
specific_library = Library.objects.get(name="Main Library")
books_in_library = specific_library.books.all()

print("\nBooks in library:", specific_library.name)
for b in books_in_library:
    print("-", b.title)

# -----------------------------------------
# 3) Retrieve the librarian for a library
# -----------------------------------------
library_librarian = specific_library.librarian  # via related_name='librarian'

print("\nLibrarian for library:", specific_library.name)
print("-", library_librarian.name)

```python
from bookshelf.models import Book
Book.objects.values("title", "author", "publication_year")
# Expected output: <QuerySet [{'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]>
```

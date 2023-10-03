from django.shortcuts import get_object_or_404, render
from .models import Book # Yerel klasördeki modeller
from django.http import Http404 # Hata sayfaları için mesela http://127.0.0.1:8000/1 gibi
from django.db.models import Avg, Max, Min # kitap sayısı hesaplarını bulmak için

# Create your views here.

def index(request):
    # books = Book.objects.all().order_by("title") # Tüm kitapları artan sıralı listeler
    books = Book.objects.all().order_by("-rating") # tüm kitapları azalan rating değerleriyle sıralayarak listeler
    num_books = books.count()
    avg_rating = books.aggregate(Avg("rating")) #rating__avg, Min("rating") -> rating__min
    return render(request, "book_outlet/index.html", {
        "books": books,
        "total_number_of_books": num_books,
        "average_rating": avg_rating
    })

def book_detail(request, slug):
    # try:
    #     book = Book.objects.get(pk=id)
    # except:
    #     raise Http404()
    book = get_object_or_404(Book, slug=slug)
    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestseller": book.is_bestselling
    })


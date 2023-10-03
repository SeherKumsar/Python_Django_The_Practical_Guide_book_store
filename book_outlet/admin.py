from django.contrib import admin
from .models import Book, Author, Address, Country

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # readonly_fields = ("slug", ) # Add Book+ da önizlemeli slug yapısı için düzenlenebilir olmalı
    prepopulated_fields = {"slug": ("title",)} # slug yapısı önizlenir
    list_filter = ("author", "rating", ) # , -> tuple değerli olduğunu belirtir bu fonk filtreleme yapar
    list_display = ("title", "author") # veri listesindeki sütunlar belirtilerek Book verisi listelenir

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Address)
admin.site.register(Country)

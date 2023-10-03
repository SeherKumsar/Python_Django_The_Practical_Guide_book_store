from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse # kitap detay sayfalarında kimlik sağlarken dinamik yapı için kullan
from django.utils.text import slugify # reverse methodu ile slug dönüşümü

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"

class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"
    
    class Meta:
        # verbose_name = tekilliği kaldırmak için kullanılır
        verbose_name_plural = "Address Entries"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # favorite_created_book veya address one-to-one olabilir
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True) # otomatik adlandırıldığı için related_name="author" gerek yoktur. db de adres henüz yok boş değerler var(null=True).

    def full_name(self):
        return self.first_name + " " + self.last_name
    
    def __str__(self):
        # return f"{self.first_name} ({self.last_name})"
        return self.full_name()


class Book(models.Model):
    title =  models.CharField(max_length=50) # metin text verisi "Harr Potter"
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    #author = models.CharField(null=True, max_length=100)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True) # Author modeliyle ilişkilendirmek için foreign key kullan ve null yazar varken kitap olabilsin
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name="books")
    # author -> one-to-many relation
    is_bestselling = models.BooleanField(default=False)
    # slug = models.SlugField(default="", null=False) # Harry Potter 1 => harry-potter-1 (slugify)
    # slug = models.SlugField(default="", null=False, db_index=True) # pk değilse primary_key=True eklenebilir
    # slug = models.SlugField(default="", blank=True, editable=False, null=False, db_index=True) # Form da boş değer girilerek veritabanında boş durum kaydedilebilir ve değer düzenlenemez
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    # published_countries = models.ManyToManyField(Country, null=False, related_name="books") # many-to-many (book-country) ilişkilerinde on_delete seçeneği eklenemez. related_name="books" eklenerek ?Country.objects.all()[0]?.book.all() gibi ilişkilendirilebilir
    published_countries = models.ManyToManyField(Country, null=False, related_name="books")

    # book-detail sayfaları için dinamik yol
    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug]) # args=[self.id] yerine slug kullan
    
    # yerleşik kaydetmeyi geçersiz kılarak super save method kullan
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.rating})"

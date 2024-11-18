from django.db import models

class BookModel(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/', blank=False, null=False)
    description = models.TextField()
    author = models.CharField(max_length=100, default='Unknown Author')
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)
    page_count = models.PositiveIntegerField(blank= True, null=True)
    keywords = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

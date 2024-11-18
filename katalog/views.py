import os
import fitz
import logging
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from collections import Counter
from .forms import BookUploadForm
from .models import BookModel



logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class BookListView(ListView):
    model = BookModel
    template_name = 'katalog/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        genre = self.request.GET.get('genre')
        favorite = self.request.GET.get('favorite')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(year__icontains=query)
            )
        
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        
        if favorite:
            queryset = queryset.filter(is_favorite=True if favorite.lower() == 'true' else False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        genres = BookModel.objects.values_list('genre', flat=True).distinct()
        
        context['genres'] = genres
        context['title'] = "Katalog"
        return context

@login_required
def favorite_books(request):
    books = BookModel.objects.filter(is_favorite=True)
    context = {
        'books': books,
        'title': "Favorite Book"
    }
    return render(request, 'favorite/index.html', context)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)

    images_dir = os.path.join(settings.MEDIA_ROOT, f'pdf_images/{book.title}')
    cover_image = None

    if os.path.exists(images_dir):
        image_files = [
            f for f in os.listdir(images_dir) if f.endswith('.png')
        ]
        if image_files:
            cover_image = os.path.join(settings.MEDIA_URL, f'pdf_images/{book.title}/{image_files[0]}')
    
    if request.method == "POST":
        if 'toggle_favorite' in request.POST:
            book.is_favorite = not book.is_favorite
            book.save()
            return redirect('katalog:book_detail', book_id=book.id)
        
        if 'delete' in request.POST:
            book.delete()
            return redirect('katalog:book_list')
    
    context = {
        'book': book,
        'cover_image': cover_image,
        'title': "Detail"
    }
    return render(request, 'katalog/book_detail.html', context)

@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            pdf_path = book.pdf_file.path
            output_dir = os.path.join(settings.MEDIA_ROOT, f'pdf_images/{book.title}')
            convert_pdf_to_images(pdf_path, output_dir)
            return redirect('katalog:book-list')
    else:
        form = BookUploadForm()
    
    context = {
        'form': form,
        'title': "Upload Book"
    }
    return render(request, 'katalog/upload_book.html', context)

def convert_pdf_to_images(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
        pix.save(image_path)
        image_paths.append(image_path)

    doc.close()
    return image_paths

@login_required
def book_edit(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)

    if request.method == "POST":
        form = BookUploadForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('katalog/book_detail.html', book_id=book.id)
    else:
        form = BookUploadForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'title': "Edit"
    }
    return render(request, 'katalog/edit_book.html', context)

def delete_book(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)
    if request.method == 'POST':
        book.delete()
    return redirect('katalog:book-list')

def toggle_favorite(request, pk):
    book = get_object_or_404(BookModel, pk=pk)
    book.is_favorite = not book.is_favorite
    book.save()
    return redirect(reverse('katalog:book-detail', args=[pk]))


def book_preview(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)
    images_dir = os.path.join(settings.MEDIA_ROOT, f'pdf_images/{book.title}')
    
    image_paths = [
        os.path.join(settings.MEDIA_URL, f'pdf_images/{book.title}/{f}')
        for f in os.listdir(images_dir) if f.endswith('.png')
    ]
    
    page_count = len(image_paths)
    page_num = int(request.GET.get('page', 1))
    if page_num < 1:
        page_num = 1
    elif page_num > page_count:
        page_num = page_count
    
    current_image = image_paths[page_num - 1]
    
    previous_disabled = page_num == 1
    next_disabled = page_num == page_count
    
    context = {
        'book': book,
        'image': current_image,
        'page_num': page_num,
        'page_count': page_count,
        'previous_disabled': previous_disabled,
        'next_disabled': next_disabled
    }
    
    return render(request, 'katalog/book_preview.html', context)


def analyze_book(request, book_id):
    book = get_object_or_404(BookModel, id=book_id)
    text = book.description
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    common_words = word_counts.most_common(10)
    
    context = {
        'title': 'Analisis',
        'book': book,
        'common_words': common_words

    }
    return render(request, 'katalog/analyze_result.html', context)
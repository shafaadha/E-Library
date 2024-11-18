from django.urls import path
from . import views

app_name = 'katalog'

urlpatterns = [
    path('upload/', views.upload_book, name='upload-book'),
    path('<int:book_id>/', views.book_detail, name='book-detail'),
    path('<int:book_id>/edit/', views.book_edit, name='book-edit'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete-book'),
    path('book/<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('book/<int:book_id>/preview/', views.book_preview, name='book-preview'),
    path('books/<int:book_id>/analyze/', views.analyze_book, name='analyze_book'),
    path('favorites/', views.favorite_books, name='favorite-book'),
    path('', views.BookListView.as_view(), name= 'book-list'),
]

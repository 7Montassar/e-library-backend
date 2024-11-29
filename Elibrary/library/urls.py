from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
urlpatterns = [
   path('', include(router.urls)),
   path('books/<int:book_id>/download/', views.download_book, name='download_book'),
]
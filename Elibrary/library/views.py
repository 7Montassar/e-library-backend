from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer
from authentication.permissions import IsAuthenticatedAndReadOnly, IsVisitorAndCanAdd, IsAdminAndCanPerformAll
import os, requests
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
load_dotenv()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def _get_google_api_credentials(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        search_engine_id = os.getenv('SEARCH_ENGINE_ID')
        if not api_key or not search_engine_id:
            raise ValueError("Google API key and Search Engine ID must be set in environment variables.")
        return api_key, search_engine_id
    
    def perform_create(self, serializer):
        title = serializer.validated_data['title']
        author = serializer.validated_data['author']
        image_url = self.get_book_cover_image(title, author)
        serializer.save(cover=image_url)
    
    def get_book_cover_image(self, title, author):
        query = f"title:{title} author:{author} book cover"
        api_url = "https://www.googleapis.com/customsearch/v1"
        api_key, search_engine_id = self._get_google_api_credentials()
        params = {
            'q': query,
            'key': api_key,
            'cx': search_engine_id ,
            'num': 1,
            'searchType': 'image'
            }
        try:
            res = requests.get(api_url, params=params)
            res.raise_for_status()
            data = res.json()
            items = data.get('items', [])
            
            if items:
                return items[0].get('link')
            else:
                return None
        except requests.RequestException as e:
            logger.error(f"Error fetching book cover image: {e}")
            return "https://example.com/placeholder.jpg"
    def get_permissions(self):
        """
        Assign permissions based on actions.
        """
        if self.action in ['list', 'retrieve']:  # Read-only actions
            permission_classes = [IsAuthenticatedAndReadOnly | IsVisitorAndCanAdd | IsAdminAndCanPerformAll]
        elif self.action == 'create':  # Add book
            permission_classes = [IsVisitorAndCanAdd | IsAdminAndCanPerformAll]
        else:  # Update and delete actions
            permission_classes = [IsAdminAndCanPerformAll]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['GET'], permission_classes=[IsAdminAndCanPerformAll])
    def admin_only(self, request):
        """
        Custom admin-only action.
        """
        return Response({"message": "Admin action performed!"})

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    response = FileResponse(book.file.open(), as_attachment=True, filename=book.file.name)
    return response

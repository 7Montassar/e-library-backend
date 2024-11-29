from rest_framework import viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from authentication.permissions import IsAdmin, IsVisitor
import os, requests
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
load_dotenv()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsVisitor]  # This allows authenticated visitors to GET and POST
    
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
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated, IsAdmin | IsVisitor]
        else:  # update, delete
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
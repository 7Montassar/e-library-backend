from rest_framework import viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from authentication.permissions import IsAdmin, IsVisitor
class BookViewSet(viewsets.ModelViewSet):
   queryset = Book.objects.all()
   serializer_class = BookSerializer
   permission_classes = [IsAuthenticated, IsVisitor]  # This allows authenticated visitors to GET and POST
   def get_permissions(self):
       """
       Instantiates and returns the list of permissions that this view requires.
       """
       if self.action in ['list', 'retrieve', 'create']:
           permission_classes = [IsAuthenticated, (IsAdmin | IsVisitor)]
       else:  # update, delete
           permission_classes = [IsAuthenticated, IsAdmin]
       return [permission() for permission in permission_classes]
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer
from authentication.permissions import IsAuthenticatedAndReadOnly, IsVisitorAndCanAdd, IsAdminAndCanPerformAll

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

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

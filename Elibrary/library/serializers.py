from rest_framework import serializers
from.models import Book
class BookSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
   class Meta:
       model = Book
       fields = ['id', 'title', 'author', 'description', 'file', 'category','cover', 'created_at']
=======
    class Meta:
        model = Book
        fields = '__all__'
        
>>>>>>> 7d4de3158162ec0a0ca42d68c9e075ec72884f60

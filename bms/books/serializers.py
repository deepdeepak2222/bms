from rest_framework import serializers
from books.models import Book, Review


class BookSerializer(serializers.ModelSerializer):
    """
    Book serializers
    """
    class Meta:
        model = Book
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Review serializer
    """
    class Meta:
        model = Review
        fields = '__all__'

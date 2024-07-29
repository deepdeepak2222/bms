# Views for book module
from django.db.models import Q
from rest_framework import viewsets, generics
from books.models import Book, Review
from books.serializers import BookSerializer, ReviewSerializer
from books.utils import get_summary_from_external_endpoint
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        summary = get_summary_from_external_endpoint(content)
        serializer.save(summary=summary)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Custom logic before deletion (e.g., logging, notifications, etc.)
        self.perform_destroy(instance)
        # Custom logic after deletion (if needed)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        try:
            book = self.get_object()
            reviews = book.reviews.all()

            # Calculate aggregated rating
            if reviews.exists():
                total_rating = sum(review.rating for review in reviews)
                avg_rating = total_rating / reviews.count()
            else:
                avg_rating = None  # Or 0 if you prefer

            response_data = {
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'year_published': book.year_published,
                'summary': book.summary,
                'average_rating': avg_rating
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RecommendationView(generics.GenericAPIView):
    """
    Read Only API to get recommended books as per user's provided params
    """
    serializer_class = BookSerializer

    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        # Retrieve user preferences from the query params
        preferred_genres = request.query_params.getlist('genres', [])
        preferred_authors = request.query_params.getlist('authors', [])
        min_rating = request.query_params.get('min_rating', 0)

        # Construct the query based on preferences
        filters = Q()
        if preferred_genres:
            filters &= Q(genre__in=preferred_genres)
        if preferred_authors:
            filters &= Q(author__in=preferred_authors)
        if min_rating:
            filters &= Q(reviews__rating__gte=min_rating)
        qs = self.get_queryset()
        # Get recommended books
        recommended_books = qs.filter(filters).distinct()

        # Serialize and return the response
        serializer = self.get_serializer(recommended_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from books.serializers import BookSerializer, ReviewSerializer
from books.views import BookViewSet, ReviewViewSet, RecommendationView
from books.models import Book, Review


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def book_serializer():
    return MagicMock(spec=BookSerializer, validated_data={'content': 'This is a test content'})


@pytest.fixture
def mock_book():
    book = MagicMock(spec=Book)
    book.id = 1
    book.title = 'Test Book'
    book.author = 'Test Author'
    book.genre = 'Fiction'
    book.year_published = 2020
    book.summary = 'A test summary'
    return book


@pytest.fixture
def mock_review(mock_book):
    review = MagicMock(spec=Review)
    review.id = 1
    review.book = mock_book
    review.rating = 4
    review.comment = 'A test comment'
    return review


class TestBookViewSet:
    view = BookViewSet

    def test_perform_create(self, book_serializer, mocker):
        view_set = self.view()
        mock_get_summary = mocker.patch('books.views.get_summary_from_external_endpoint', return_value='Mocked Summary')
        # Perform the creation with the mock serializer
        view_set.perform_create(book_serializer)
        # Assert that the summary function was called with the correct content
        mock_get_summary.assert_called_once_with('This is a test content')
        # Assert that the serializer's save method was called with the correct summary
        book_serializer.save.assert_called_once_with(summary='Mocked Summary')

    def test_destroy(self, api_client, mock_book, mocker):
        mocker.patch.object(BookViewSet, 'get_object', return_value=mock_book)
        mocker.patch.object(BookViewSet, 'perform_destroy')

        # Simulate the delete request
        response = api_client.delete(reverse('book-detail', kwargs={'pk': mock_book.id}))

        # Assertions to check the flow
        assert response.status_code == status.HTTP_204_NO_CONTENT
        BookViewSet.perform_destroy.assert_called_once_with(mock_book)

    def test_summary(self, api_client, mock_book, mocker):
        # Mocking BookViewSet.get_object to return the mock_book
        mocker.patch.object(BookViewSet, 'get_object', return_value=mock_book)

        # Mocking the related manager 'reviews' to simulate the behavior of Django's related manager
        mock_reviews = mocker.MagicMock()
        mock_reviews.exists.return_value = True
        mock_reviews.count.return_value = 1
        mock_reviews.all.return_value = [MagicMock(rating=4)]

        # Attaching the mocked reviews manager to the mock_book
        mock_book.reviews = mock_reviews

        response = api_client.get(reverse('book-summary', kwargs={'pk': mock_book.id}))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['average_rating'] == 4


class TestReviewViewSet:
    def test_create_review(self, api_client, mock_book, mocker):
        mocker.patch('books.models.Review.objects.create')

        response = api_client.post(
            reverse('review-list'),
            {
                'book': mock_book.id,
                'rating': 5,
                'comment': 'Great book!'
            },
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        Review.objects.create.assert_called_once_with(book=mock_book, rating=5, comment='Great book!')

    def test_destroy_review(self, api_client, mock_review, mocker):
        mocker.patch.object(ReviewViewSet, 'get_object', return_value=mock_review)
        mocker.patch.object(ReviewViewSet, 'perform_destroy')

        response = api_client.delete(reverse('review-detail', kwargs={'pk': mock_review.id}))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        ReviewViewSet.perform_destroy.assert_called_once_with(mock_review)


class TestRecommendationView:
    def test_recommendation(self, api_client, mock_book, mocker):
        mocker.patch('books.views.Book.objects.all', return_value=[mock_book])

        response = api_client.get(
            reverse('recommendation'),
            {
                'genres': ['Fiction'],
                'min_rating': 3
            },
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == mock_book.title

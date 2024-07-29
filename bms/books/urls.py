from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, ReviewViewSet, RecommendationView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', RecommendationView.as_view(), name='book-recommendations'),
]

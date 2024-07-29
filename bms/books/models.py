from django.db import models


class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining auto-incrementing id
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year_published = models.IntegerField()
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)


class Review(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining auto-incrementing id
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    review_text = models.TextField()
    rating = models.IntegerField()

    class Meta:
        # A user's review on a book should be unique
        unique_together = ('user_id', 'book')

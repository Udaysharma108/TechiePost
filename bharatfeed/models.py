from django.db import models
from django.utils import timezone

class TechArticle(models.Model):
    title = models.CharField(max_length=255)
    source_url = models.URLField(unique=True)
    content_raw = models.TextField()
    cleaned_summary = models.TextField(blank=True, null=True)
    
    category = models.CharField(max_length=100, default='General Tech')
    language_code = models.CharField(max_length=10, default='en')
    
    fetched_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tech_articles'
        ordering = ['-fetched_at']
        indexes = [
            models.Index(fields=['source_url']),
            models.Index(fields=['fetched_at']),
        ]

    def __str__(self):
        return f"[{self.category}] {self.title[:40]}"
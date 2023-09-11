from django.db import models

# Create your models here.
class urlShortener(models.Model):
    long_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=10)
    click_count = models.IntegerField(null = True, default=0)
    user_platform = models.CharField(max_length=200)
    user_browser = models.CharField(max_length=200)
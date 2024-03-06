from django.db import models

# Create your models here.
class FilmInfo(models.Model):
    course = models.CharField(verbose_name='課程名稱', max_length=20)
    lecturer = models.CharField(verbose_name='授課者', max_length=20)
    url = models.URLField(verbose_name='網址', max_length=256)
    
class PhaseDescription(models.Model):
    start = models.CharField(verbose_name='起始時間', max_length=12)
    end = models.CharField(verbose_name='結尾時間', max_length=12)
    description = models.CharField(verbose_name='段落重點', max_length=60)
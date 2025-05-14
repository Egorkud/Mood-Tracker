from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ("happy", "Веселий"),
        ("sad", "Сумний"),
        ("angry", "Злий"),
        ("neutral", "Нейтральний"),
        ("excited", "Задоволений"),
        ("anxious", "Тривожний"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mood_entries")
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = "Запис про настрій"
        verbose_name_plural = "Записи про настрої"

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.mood}"
from django.contrib import admin

from .models import MoodEntry, EmailVerificationCode

# Register your models here.
admin.site.register(MoodEntry)
admin.site.register(EmailVerificationCode)
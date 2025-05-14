from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MoodEntryViewSet

router = DefaultRouter()
router.register(r'mood', MoodEntryViewSet, basename='mood')

urlpatterns = [
    path('', include(router.urls)),
]

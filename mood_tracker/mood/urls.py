from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MoodEntryViewSet
from .views import RequestCodeView, VerifyCodeView

router = DefaultRouter()
router.register(r'mood', MoodEntryViewSet, basename='mood')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('auth/request-code/', RequestCodeView.as_view(), name='request-code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import MoodEntryViewSet
from .views import RequestCodeView, VerifyCodeView

router = DefaultRouter()
router.register(r'mood', MoodEntryViewSet, basename='mood')

urlpatterns = [
    path('', include(router.urls)),
    path('login', views.login_page, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/create-entry/', views.create_mood_entry, name='create-entry'),
]

urlpatterns += [
    path('auth/request-code/', RequestCodeView.as_view(), name='request-code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]
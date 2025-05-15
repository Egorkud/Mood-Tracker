from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import RequestCodeView, VerifyCodeView, CreateMoodEntryView, UserInfoView, MoodEntryViewSet

router = DefaultRouter()
router.register(r'mood', MoodEntryViewSet, basename='mood')

urlpatterns = [
    path('', include(router.urls)),
    path('login', views.login_page, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/mood/create/', CreateMoodEntryView.as_view(), name='create_mood'),
    path('api/user-info/', UserInfoView.as_view(), name='user_info'),
    path("api/mood/week/", views.weekly_mood),

]

urlpatterns += [
    path('auth/request-code/', RequestCodeView.as_view(), name='request-code'),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]

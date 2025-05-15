import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailVerificationCode
from .models import MoodEntry
from .serializers import EmailRequestSerializer, CodeVerificationSerializer
from .serializers import MoodEntrySerializer


# Create your views here.
def login_page(request):
    return render(request, 'mood/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'mood/dashboard.html')


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Повертаємо тільки записи користувача, що виконує запит
        return MoodEntry.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        # Автоматично прив'язуємо запис до користувача
        serializer.save(user=self.request.user)


class RequestCodeView(generics.CreateAPIView):
    serializer_class = EmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(username=email, email=email)
        code = str(random.randint(100000, 999999))

        EmailVerificationCode.objects.update_or_create(user=user, defaults={'code': code})

        # Поки що просто виводимо код у консоль
        print(f"[DEBUG] Verification code for {email}: {code}")

        return Response({"message": "Verification code sent successfully."})


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = CodeVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
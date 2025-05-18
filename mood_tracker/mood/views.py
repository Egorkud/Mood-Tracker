import random
from collections import Counter
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailVerificationCode, MoodEntry
from .serializers import EmailRequestSerializer, CodeVerificationSerializer, MoodEntrySerializer


# Create your views here.
def login_page(request):
    return render(request, 'mood/login.html')


def dashboard_view(request):
    return render(request, 'mood/dashboard.html', {
        'user': request.user.username,
    })


class WeeklyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        week_ago = today - timedelta(days=7)

        entries = MoodEntry.objects.filter(user=request.user, date__gte=week_ago)

        mood_counts = Counter(entry.mood for entry in entries)
        total_entries = len(entries)

        mood_to_score = {
            "😄": 5,
            "🙂": 4,
            "😐": 3,
            "☹️": 2,
            "😢": 1,
            "❓": 0
        }

        mood_scores = [mood_to_score.get(entry.mood, 3) for entry in entries]
        average_mood = round(sum(mood_scores) / total_entries, 1) if total_entries else 0

        most_common_emotion = mood_counts.most_common(1)[0][0] if total_entries else "Немає даних"
        emoji = ""
        for key, value in mood_to_score.items():
            if value == average_mood:
                emoji = key
                break

        return Response({
            "from": str(week_ago),
            "to": str(today),
            "entries_count": total_entries,
            "mood_counts": mood_counts,
            "average_mood": average_mood,
            "most_common_emotion": most_common_emotion,
            "emotion_image": emoji
        })


@api_view(['POST'])
def telegram_login(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "username": user.username,
        })
    except User.DoesNotExist:
        return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_mood(request):
    today = date.today()
    week_ago = today - timedelta(days=6)  # 7 днів включно
    entries = MoodEntry.objects.filter(user=request.user, date__range=(week_ago, today)).order_by('date')
    data = [{"date": e.date.strftime("%d-%m"), "mood": e.mood} for e in entries]
    return Response(data)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username})


class CreateMoodEntryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        mood = data.get('mood')
        note = data.get('note')
        date = data.get('date')

        if not mood or not date:
            return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

        MoodEntry.objects.create(
            user=request.user,
            mood=mood,
            note=note,
            date=date
        )

        return Response({'status': 'ok'})


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Повертаємо тільки записи користувача, що виконує запит
        return MoodEntry.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        # Автоматично прив'язуємо запис до користувача
        print("[DEBUG] Current user:", self.request.user)
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

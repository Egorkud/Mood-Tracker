import random

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MoodEntry, EmailVerificationCode


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['id', 'user', 'date', 'mood', 'note']
        read_only_fields = ['id', 'user']

class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']
        user, created = User.objects.get_or_create(username=email, email=email)
        code = str(random.randint(100000, 999999))

        EmailVerificationCode.objects.update_or_create(user=user, defaults={'code': code})

        # Тут можна додати надсилання коду на email або вивід у консоль
        print(f"[DEBUG] Код для {email}: {code}")

        return {"message": "Verification code sent."}


class CodeVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            user = User.objects.get(email=email)
            record = EmailVerificationCode.objects.get(user=user)

            if record.code != code:
                raise serializers.ValidationError("Incorrect code")

        except (User.DoesNotExist, EmailVerificationCode.DoesNotExist):
            raise serializers.ValidationError("Invalid email or code")

        data['user'] = user
        return data
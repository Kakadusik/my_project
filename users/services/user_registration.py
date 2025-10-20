from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserRegistrationService:
    """
    Сервис для регистрации пользователей
    """

    @staticmethod
    def register_user(username, email, password, first_name="", last_name=""):
        """Регистрация нового пользователя"""
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return user

    @staticmethod
    def update_user_profile(user_id, **kwargs):
        """Обновление профиля пользователя"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Пользователь не найден")

        allowed_fields = ["first_name", "last_name", "email"]

        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)

        user.save()
        return user

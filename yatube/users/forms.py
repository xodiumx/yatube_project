from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    """Создаем форму для регистрации"""
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )

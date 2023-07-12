from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """Custom User creation form"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
            'is_ai',
        )


class CustomUserChangeForm(UserChangeForm):
    """Custom User change form"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
            'is_ai',
        )

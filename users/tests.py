import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from app_common.models import BaseModel
from users.models import CustomUserModel, VerificationModel, ProfileModel, FollowModel

User = get_user_model()

@pytest.mark.django_db
def test_custom_user_model_creation():
    """Ismoil, bu test CustomUserModel yaratishni sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    assert user.email == "ismoil@example.com"
    assert user.username == "ismoil"
    assert user.check_password("testpass123") is True

@pytest.mark.django_db
def test_get_tokens():
    """Ismoil, bu test get_tokens metodini sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    tokens = user.get_tokens()
    assert "refresh" in tokens
    assert "access" in tokens
    assert isinstance(tokens["refresh"], str)
    assert isinstance(tokens["access"], str)

@pytest.mark.django_db
def test_get_verification():
    """Ismoil, bu test get_verification metodini sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    code = user.get_verification(expire_minutes=2)
    assert 1000 <= code <= 9999  # Kod 4 xonali bo‘lishi kerak
    verification = VerificationModel.objects.get(user=user)
    assert verification.code == code
    assert verification.expire_minutes == 2

@pytest.mark.django_db
def test_verification_model_str():
    """Ismoil, bu test VerificationModel __str__ metodini sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    verification = VerificationModel.objects.create(user=user, code=1234, expire_minutes=2)
    assert str(verification) == "1234"

@pytest.mark.django_db
def test_profile_model_creation():
    """Ismoil, bu test ProfileModel yaratishni sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    profile = ProfileModel.objects.create(
        user=user,
        short_bio="Salom, men Ismoilman!",
        about="Django bilan ishlayman.",
        pronouns="u/o‘zi"
    )
    assert profile.user == user
    assert profile.short_bio == "Salom, men Ismoilman!"
    assert profile.__str__() == "ismoil"

@pytest.mark.django_db
def test_profile_model_avatar_validation():
    """Ismoil, bu test avatar uchun FileExtensionValidator’ni sinaydi."""
    user = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    profile = ProfileModel(user=user, short_bio="Test bio", about="Test about")
    with pytest.raises(Exception):  # Noto‘g‘ri kengaytma uchun xato chiqishi kerak
        profile.avatar = "test.pdf"  # Faqat png, jpg, gif ruxsat etilgan
        profile.full_clean()

@pytest.mark.django_db
def test_follow_model_creation():
    """Ismoil, bu test FollowModel yaratishni sinaydi."""
    user1 = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    user2 = User.objects.create_user(username="ali", email="ali@example.com", password="testpass123")
    follow = FollowModel.objects.create(from_user=user1, to_user=user2)
    assert follow.from_user == user1
    assert follow.to_user == user2
    assert str(follow) == "ismoil following to ali"

@pytest.mark.django_db
def test_follow_model_relationships():
    """Ismoil, bu test following va followers related_name’larini sinaydi."""
    user1 = User.objects.create_user(username="ismoil", email="ismoil@example.com", password="testpass123")
    user2 = User.objects.create_user(username="ali", email="ali@example.com", password="testpass123")
    FollowModel.objects.create(from_user=user1, to_user=user2)
    assert user1.following.count() == 1
    assert user2.followers.count() == 1
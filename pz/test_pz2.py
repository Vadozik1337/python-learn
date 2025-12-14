# PZ4
import pytest
from pz2 import User, Administrator, RegularUser, AccessControl



def test_verify_password_success():
    """Перевірка правильного пароля"""
    user = User("test_user", "password123")
    assert user.verify_password("password123") is True


def test_verify_password_failure():
    """Перевірка неправильного пароля"""
    user = User("test_user", "password123")
    assert user.verify_password("wrong_pass") is False


def test_add_permission_new():
    """Додавання нового дозволу"""
    admin = Administrator("admin", "pass")
    admin.add_permission("delete_users")
    assert "delete_users" in admin.permissions
    assert len(admin.permissions) == 1


def test_add_permission_duplicate():
    """Спроба додати дозвіл, який вже існує (не має дублюватися)"""
    admin = Administrator("admin", "pass", permissions=["read"])
    admin.add_permission("read")
    # Список не повинен збільшитись
    assert len(admin.permissions) == 1
    assert admin.permissions == ["read"]



def test_authenticate_success():
    """Успішний вхід"""
    system = AccessControl()
    user = RegularUser("ivan", "secret")
    system.add_user(user)

    authenticated_user = system.authenticate_user("ivan", "secret")
    assert authenticated_user is not None
    assert authenticated_user.username == "ivan"
    assert authenticated_user.last_login_date is not None


def test_authenticate_wrong_password():
    """Вхід з неправильним паролем"""
    system = AccessControl()
    user = User("ivan", "secret")
    system.add_user(user)

    authenticated_user = system.authenticate_user("ivan", "wrong")
    assert authenticated_user is None


def test_authenticate_user_not_found():
    """Користувача не існує"""
    system = AccessControl()
    authenticated_user = system.authenticate_user("ghost", "123")
    assert authenticated_user is None


def test_authenticate_inactive_user():
    """Користувач деактивований"""
    system = AccessControl()
    user = User("ivan", "secret")
    user.is_active = False  # Деактивуємо вручну
    system.add_user(user)

    authenticated_user = system.authenticate_user("ivan", "secret")
    assert authenticated_user is None


def test_add_user_success():
    """Додавання нового юзера"""
    system = AccessControl()
    user = User("new_user", "123")
    system.add_user(user)
    assert "new_user" in system.users


def test_add_user_existing(capsys):
    """Спроба додати існуючого юзера (має вивести помилку)"""
    system = AccessControl()
    user = User("user1", "123")
    system.add_user(user)

    user_duplicate = User("user1", "456")
    system.add_user(user_duplicate)

    assert system.users["user1"].verify_password("123") is True
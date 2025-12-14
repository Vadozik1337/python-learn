import hashlib
from datetime import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = True  # За замовчуванням активний

    def _hash_password(self, password):
        """Внутрішній метод для хешування пароля (SHA-256)."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Перевіряє, чи співпадає введений пароль зі збереженим хешем."""
        return self.password_hash == self._hash_password(password)

    def __str__(self):
        return f"User({self.username}, Role: {self.__class__.__name__})"


class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions if permissions else []

    def add_permission(self, permission):
        if permission not in self.permissions:
            self.permissions.append(permission)


class RegularUser(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.last_login_date = None

    def update_login_date(self):
        self.last_login_date = datetime.now()


class GuestUser(User):
    def __init__(self, username="Guest"):
        super().__init__(username, password="")
        self.access_level = "limited"


class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        """Додає нового користувача до системи."""
        if user.username in self.users:
            print(f"Помилка: Користувач {user.username} вже існує.")
            return
        self.users[user.username] = user
        print(f"Користувача {user.username} додано.")

    def authenticate_user(self, username, password):
        """
        Перевіряє ім'я та пароль.
        Повертає об'єкт користувача, якщо успішно, або None.
        """
        user = self.users.get(username)

        if not user:
            print(f"Аутентифікація не вдалася: Користувача {username} не знайдено.")
            return None

        if not user.is_active:
            print(f"Аутентифікація не вдалася: Обліковий запис {username} деактивовано.")
            return None

        if user.verify_password(password):
            print(f"Успішний вхід: {username}")
            if isinstance(user, RegularUser):
                user.update_login_date()
            return user
        else:
            print(f"Аутентифікація не вдалася: Невірний пароль для {username}.")
            return None



if __name__ == "__main__":
    system = AccessControl()

    admin = Administrator("admin_max", "adminPass123", permissions=["all"])
    user1 = RegularUser("ivan_p", "mySecretPass")
    guest = GuestUser()

    system.add_user(admin)
    system.add_user(user1)
    system.add_user(guest)

    print("-" * 30)

    current_user = system.authenticate_user("ivan_p", "mySecretPass")

    system.authenticate_user("admin_max", "wrongPassword")

    system.authenticate_user("hacker", "12345")

    print("-" * 30)

    if isinstance(current_user, RegularUser):
        print(f"Останній вхід користувача {current_user.username}: {current_user.last_login_date}")
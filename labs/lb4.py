import sqlite3
import hashlib

DB_NAME = "users.db"


def create_db():
    """
    Пункт 1: Створення БД та таблиці.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       login
                       TEXT
                       PRIMARY
                       KEY,
                       password
                       TEXT
                       NOT
                       NULL,
                       full_name
                       TEXT
                       NOT
                       NULL
                   )
                   ''')

    conn.commit()
    conn.close()
    print(f"База даних '{DB_NAME}' та таблиця успішно ініціалізовані.")


def hash_password(password):
    """
    Допоміжна функція для хешування паролю (SHA-256).
    Пункт 1b: пароль зберігається у вигляді хешу.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(login, password, full_name):
    """
    Пункт 2a: Додавання нових користувачів.
    """
    hashed_pw = hash_password(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
                       (login, hashed_pw, full_name))

        conn.commit()
        print(f"Користувача {login} успішно додано!")

    except sqlite3.IntegrityError:
        print(f"Помилка: Користувач з логіном '{login}' вже існує.")
    finally:
        conn.close()


def update_password(login, new_password):
    """
    Пункт 2b: Оновлення паролю користувачів.
    """
    hashed_pw = hash_password(new_password)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed_pw, login))

    if cursor.rowcount > 0:
        conn.commit()
        print(f"Пароль для користувача {login} успішно оновлено.")
    else:
        print(f"Користувача {login} не знайдено.")

    conn.close()


def authenticate_user():
    """
    Пункт 2c: Перевірка автентифікації.
    Зчитування за допомогою input().
    """
    print("\n--- Вхід у систему ---")
    login_input = input("Введіть логін: ")
    password_input = input("Введіть пароль: ")

    hashed_input = hash_password(password_input)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password, full_name FROM users WHERE login = ?", (login_input,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password_hash, full_name = result
        if stored_password_hash == hashed_input:
            print(f"Успішний вхід! Ласкаво просимо, {full_name}.")
            return True
        else:
            print("Невірний пароль.")
            return False
    else:
        print("Користувача з таким логіном не знайдено.")
        return False


if __name__ == "__main__":
    create_db()

    print("\n--- Додавання користувачів ---")
    add_user("user1", "mypassword123", "Іванов Іван Іванович")
    add_user("admin", "adminpass", "Адмін Адмінович")

    authenticate_user()

    print("\n--- Зміна паролю ---")
    update_password("user1", "new_secure_pass")

    authenticate_user()
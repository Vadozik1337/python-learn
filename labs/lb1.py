import string
import hashlib

inventory = {"Яблука": 50, "Молоко": 4, "Хліб": 10}
tasks = {"Написати звіт": "виконано", "Купити каву": "в процесі"}
users_db = {}


def analyze_text():
    print("\n--- 1. Робота з текстом ---")
    text = input("Введіть текст для аналізу: ")

    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator).lower()
    words = clean_text.split()

    word_dict = {}
    for word in words:
        word_dict[word] = word_dict.get(word, 0) + 1

    print(f"\nЧастота слів: {word_dict}")

    frequent_words = [word for word, count in word_dict.items() if count > 3]
    print(f"Слова, що зустрічаються більше 3 разів: {frequent_words}")
    input("\nНатисніть Enter, щоб продовжити...")


def manage_inventory():
    print("\n--- 2. Інвентаризація продуктів ---")
    print(f"Поточний склад: {inventory}")

    try:
        prod = input("Введіть назву продукту: ")
        qty = int(input("Введіть кількість (+ додати, - списати): "))

        if prod in inventory:
            inventory[prod] += qty
        elif qty > 0:
            inventory[prod] = qty

        if inventory.get(prod, 0) < 0:
            inventory[prod] = 0

        print(f"Оновлений склад: {inventory}")

        low_stock = [p for p, q in inventory.items() if q < 5]
        print(f"Мало товару (менше 5): {low_stock}")

    except ValueError:
        print("Помилка: кількість має бути числом.")
    input("\nНатисніть Enter, щоб продовжити...")


def sales_statistics():
    print("\n--- 3. Статистика продажів ---")
    sales = [
        {"продукт": "Ноутбук", "кількість": 2, "ціна": 20000},
        {"продукт": "Мишка", "кількість": 10, "ціна": 500},
        {"продукт": "Клавіатура", "кількість": 3, "ціна": 800},
        {"продукт": "Монітор", "кількість": 1, "ціна": 5000}
    ]
    print("Список продажів:", sales)

    revenue_dict = {}
    for sale in sales:
        prod = sale["продукт"]
        total = sale["кількість"] * sale["ціна"]
        revenue_dict[prod] = revenue_dict.get(prod, 0) + total

    print(f"\nЗагальний дохід по товарах: {revenue_dict}")

    high_revenue = [prod for prod, rev in revenue_dict.items() if rev > 1000]
    print(f"Продукти з доходом > 1000: {high_revenue}")
    input("\nНатисніть Enter, щоб продовжити...")


def manage_tasks():
    print("\n--- 4. Система управління задачами ---")
    print(f"Поточні задачі: {tasks}")
    print("Дії: 1-Додати, 2-Змінити статус, 3-Видалити, 4-Показати 'очікує'")

    choice = input("Ваш вибір: ")

    if choice == '1':
        name = input("Назва задачі: ")
        status = input("Статус (очікує/в процесі/виконано): ")
        tasks[name] = status
    elif choice == '2':
        name = input("Назва задачі: ")
        if name in tasks:
            status = input("Новий статус: ")
            tasks[name] = status
        else:
            print("Задачу не знайдено.")
    elif choice == '3':
        name = input("Назва задачі для видалення: ")
        if name in tasks:
            del tasks[name]
    elif choice == '4':
        pending = [n for n, s in tasks.items() if s == "очікує"]
        print(f"Задачі в очікуванні: {pending}")

    print(f"Оновлений список: {tasks}")
    input("\nНатисніть Enter, щоб продовжити...")


def auth_system():
    print("\n--- 5. Аутентифікація користувачів ---")
    action = input("1 - Реєстрація, 2 - Вхід: ")

    if action == '1':
        login = input("Придумайте логін: ")
        if login in users_db:
            print("Такий користувач вже існує!")
            return
        password = input("Придумайте пароль: ")
        fullname = input("Ваше ПІБ: ")

        pass_hash = hashlib.md5(password.encode()).hexdigest()
        users_db[login] = {"password": pass_hash, "fullname": fullname}
        print("Реєстрація успішна!")

    elif action == '2':
        login = input("Логін: ")
        password = input("Пароль: ")

        if login in users_db:
            input_hash = hashlib.md5(password.encode()).hexdigest()
            if input_hash == users_db[login]["password"]:
                print(f"Успішний вхід! Вітаємо, {users_db[login]['fullname']}")
            else:
                print("Невірний пароль.")
        else:
            print("Користувача не знайдено.")

    input("\nНатисніть Enter, щоб продовжити...")


def main():
    while True:
        print("\n" * 2)
        print("=" * 30)
        print(" ГОЛОВНЕ МЕНЮ")
        print("=" * 30)
        print("1. Аналіз тексту")
        print("2. Склад продуктів")
        print("3. Статистика продажів")
        print("4. Менеджер задач")
        print("5. Вхід / Реєстрація")
        print("0. Вихід")
        print("=" * 30)

        choice = input("Оберіть пункт меню: ")

        if choice == '1':
            analyze_text()
        elif choice == '2':
            manage_inventory()
        elif choice == '3':
            sales_statistics()
        elif choice == '4':
            manage_tasks()
        elif choice == '5':
            auth_system()
        elif choice == '0':
            print("До побачення!")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()
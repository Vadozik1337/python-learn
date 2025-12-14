import sqlite3
from datetime import datetime, timedelta

DB_NAME = "security_logs.db"


def create_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


# --- ЗАВДАННЯ 1: Створення таблиць (без змін) ---
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS EventSources
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       name
                       TEXT
                       UNIQUE,
                       location
                       TEXT,
                       type
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS EventTypes
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       type_name
                       TEXT
                       UNIQUE,
                       severity
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS SecurityEvents
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       timestamp
                       TEXT, -- Змінили підказку типу на TEXT, оскільки SQLite зберігає дати як рядки
                       source_id
                       INTEGER,
                       event_type_id
                       INTEGER,
                       message
                       TEXT,
                       ip_address
                       TEXT,
                       username
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       source_id
                   ) REFERENCES EventSources
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       event_type_id
                   ) REFERENCES EventTypes
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    conn.close()
    print("Таблиці перевірено/створено.")


# --- ЗАВДАННЯ 2 & 3: Наповнення даними (ВИПРАВЛЕНО) ---
def populate_initial_data():
    conn = create_connection()
    cursor = conn.cursor()

    # 2. Типи подій
    event_types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]

    for et in event_types:
        try:
            cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", et)
        except sqlite3.IntegrityError:
            pass

            # 3. Джерела подій
    event_sources = [
        ("Firewall_Main", "Server Room A", "Firewall"),
        ("Web_Server_01", "Cloud Region EU", "Web Server"),
        ("IDS_Sensor_Office", "Office HQ", "IDS"),
        ("Auth_Server", "Server Room B", "Auth Service")
    ]

    for es in event_sources:
        try:
            cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", es)
        except sqlite3.IntegrityError:
            pass

    conn.commit()

    # Отримуємо ID
    def get_id(table, col, val):
        cursor.execute(f"SELECT id FROM {table} WHERE {col}=?", (val,))
        res = cursor.fetchone()
        return res[0] if res else None

    fw_id = get_id("EventSources", "name", "Firewall_Main")
    web_id = get_id("EventSources", "name", "Web_Server_01")
    auth_id = get_id("EventSources", "name", "Auth_Server")

    login_fail_id = get_id("EventTypes", "type_name", "Login Failed")
    malware_id = get_id("EventTypes", "type_name", "Malware Alert")
    scan_id = get_id("EventTypes", "type_name", "Port Scan Detected")

    # --- ВИПРАВЛЕННЯ ТУТ: Конвертуємо дати в рядки ---
    now = datetime.now()
    one_hour_ago = now - timedelta(minutes=45)
    two_days_ago = now - timedelta(days=2)

    # Формат для SQLite: "YYYY-MM-DD HH:MM:SS"
    fmt = "%Y-%m-%d %H:%M:%S"

    t_now = now.strftime(fmt)
    t_1h = one_hour_ago.strftime(fmt)
    t_2d = two_days_ago.strftime(fmt)

    events_data = [
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),
        (t_1h, auth_id, login_fail_id, "Wrong password provided", "192.168.1.50", "admin"),

        (t_now, web_id, malware_id, "Trojan detected in /tmp", "10.0.0.5", None),
        (t_2d, fw_id, scan_id, "Port 22 scan detected", "45.33.22.11", None),
        (t_2d, web_id, malware_id, "Ransomware signature found", "10.0.0.5", "www-data"),
        (t_now, auth_id, login_fail_id, "User not found", "172.16.0.1", "guest"),
        (t_now, fw_id, scan_id, "ICMP Flood", "192.168.1.100", None)
    ]

    cursor.execute("SELECT count(*) FROM SecurityEvents")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
                           INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', events_data)
        print("Тестові дані успішно додано.")

    conn.commit()
    conn.close()


# --- ЗАВДАННЯ 4 ---

def register_event_source(name, location, src_type):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)",
                       (name, location, src_type))
        conn.commit()
        print(f"Джерело '{name}' додано.")
    except sqlite3.IntegrityError:
        print(f"Джерело '{name}' вже існує.")
    finally:
        conn.close()


def register_event_type(type_name, severity):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)",
                       (type_name, severity))
        conn.commit()
        print(f"Тип '{type_name}' додано.")
    except sqlite3.IntegrityError:
        print(f"Тип '{type_name}' вже існує.")
    finally:
        conn.close()


# --- ВИПРАВЛЕННЯ ТУТ: Конвертуємо поточний час в рядок ---
def log_security_event(source_name, event_type_name, message, ip_address=None, username=None):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source_name,))
    src_res = cursor.fetchone()
    cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type_name,))
    type_res = cursor.fetchone()

    if src_res and type_res:
        # Явно перетворюємо datetime в рядок
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
                       INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (timestamp, src_res[0], type_res[0], message, ip_address, username))
        conn.commit()
        print("Подію залоговано.")
    else:
        print("Помилка: Невірні дані.")
    conn.close()


# Функції пошуку (без змін, бо вони тільки читають дані)
def get_recent_login_failures():
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
            SELECT se.timestamp, es.name, se.ip_address, se.username
            FROM SecurityEvents se
                     JOIN EventTypes et ON se.event_type_id = et.id
                     JOIN EventSources es ON se.source_id = es.id
            WHERE et.type_name = 'Login Failed'
              AND se.timestamp >= datetime('now', '-24 hours') \
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    print("\n--- Login Failed (24h) ---")
    for row in results: print(row)
    return results


def detect_brute_force_attempts():
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
            SELECT se.ip_address, COUNT(*) as attempts
            FROM SecurityEvents se
                     JOIN EventTypes et ON se.event_type_id = et.id
            WHERE et.type_name = 'Login Failed'
              AND se.timestamp >= datetime('now', '-1 hours')
            GROUP BY se.ip_address
            HAVING attempts > 5 \
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    print("\n--- Brute Force Check ---")
    for row in results: print(f"IP: {row[0]}, Спроб: {row[1]}")
    return results


def get_critical_events_weekly():
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
            SELECT es.name, et.type_name, se.message, se.timestamp
            FROM SecurityEvents se
                     JOIN EventTypes et ON se.event_type_id = et.id
                     JOIN EventSources es ON se.source_id = es.id
            WHERE et.severity = 'Critical'
              AND se.timestamp >= datetime('now', '-7 days')
            ORDER BY es.name \
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    print("\n--- Critical Events (Weekly) ---")
    for row in results: print(f"{row[0]} | {row[1]} | {row[3]}")
    return results


def search_events_by_keyword(keyword):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''
            SELECT se.timestamp, et.type_name, se.message
            FROM SecurityEvents se
                     JOIN EventTypes et ON se.event_type_id = et.id
            WHERE se.message LIKE ? \
            '''
    cursor.execute(query, (f'%{keyword}%',))
    results = cursor.fetchall()
    conn.close()
    print(f"\n--- Search: '{keyword}' ---")
    for row in results: print(row)
    return results


if __name__ == "__main__":
    create_tables()
    populate_initial_data()

    print("\n--- Демонстрація ---")
    register_event_source("VPN_Gateway", "Remote", "VPN Concentrator")
    register_event_type("DDoS Attempt", "Critical")
    log_security_event("VPN_Gateway", "Login Success", "User connected via VPN", "203.0.113.5", "manager")

    get_recent_login_failures()
    detect_brute_force_attempts()
    get_critical_events_weekly()
    search_events_by_keyword("Trojan")
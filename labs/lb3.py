import hashlib

def analyze_log_file(log_file_path):

    results = {}

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 9:
                    continue
                code = parts[-2]
                if code.isdigit():
                    results[code] = results.get(code, 0) + 1

        return results

    except FileNotFoundError:
        print(f"[Помилка] Файл '{log_file_path}' не знайдено.")
        return {}
    except IOError:
        print(f"[Помилка] Не вдалося прочитати файл '{log_file_path}'.")
        return {}

def generate_file_hashes(*file_paths):
    hashes = {}

    for path in file_paths:
        try:
            with open(path, 'rb') as file:
                content = file.read()
                file_hash = hashlib.sha256(content).hexdigest()
                hashes[path] = file_hash
        except FileNotFoundError:
            print(f"[Помилка] Файл '{path}' не знайдено.")
        except IOError:
            print(f"[Помилка] Не вдалося прочитати файл '{path}'.")

    return hashes


def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {ip: 0 for ip in allowed_ips}

    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                parts = line.strip().split()
                if not parts:
                    continue
                ip = parts[0]
                if ip in ip_counts:
                    ip_counts[ip] += 1

    except FileNotFoundError:
        print(f"[Помилка] Вхідний файл '{input_file_path}' не знайдено.")
        return
    except IOError:
        print(f"[Помилка] Не вдалося прочитати файл '{input_file_path}'.")
        return

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for ip, count in ip_counts.items():
                outfile.write(f"{ip} - {count}\n")

        print(f"[OK] Результати записано у файл '{output_file_path}'.")

    except IOError:
        print(f"[Помилка] Не вдалося записати до файлу '{output_file_path}'.")



if __name__ == "__main__":
    log_path = "apache_logs.txt"

    print("=== Завдання 1: Аналіз кодів HTTP ===")
    codes = analyze_log_file(log_path)
    for code, count in codes.items():
        print(f"{code}: {count}")

    print("\n=== Завдання 2: Хеш SHA-256 ===")
    hashes = generate_file_hashes(log_path)
    for file, h in hashes.items():
        print(f"{file}: {h}")

    print("\n=== Завдання 3: Фільтрація IP ===")
    allowed = ["83.149.9.216", "66.249.73.135", "105.235.130.196"]
    filter_ips(log_path, "../filtered_ips.txt", allowed)

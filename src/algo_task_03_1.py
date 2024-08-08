import hashlib
import os
import shutil
import sys


def copy_files(source_dir: str, dest_dir: str) -> None:
    """
    Копіює файли з вихідної директорії у цільову, сортуючи по суб-теках (піддеректоріях) відповідно до розширення файлів.

    Parameters
    ----------
    source_dir : str
        Шлях до вихідної директорії.
    dest_dir : str
        Шлях до цільової директорії.
    """
    try:
        # Перебираємо всі елементи у вихідній директорії
        for item in os.listdir(source_dir):
            # Повний шлях до елемента
            item_path = os.path.join(source_dir, item)

            # Перевіряємо, чи є елемент директорією
            if os.path.isdir(item_path):
                # Якщо елемент є директорією, викликаємо функцію рекурсивно
                copy_files(item_path, dest_dir)

            # Перевіряємо, чи є елемент файлом
            elif os.path.isfile(item_path):
                # Отримуємо розширення файлу без крапки
                file_extension = os.path.splitext(item)[1][1:]

                # Перевіряємо, чи у файла є розширення
                # (якщо немає, буде скопійовано в теку призначення без окремої піддиректорії)
                if file_extension:
                    # Створюємо шлях до нової піддиректорії на основі розширення файлу
                    extension_dir = os.path.join(dest_dir, file_extension)
                    # Створюємо піддиректорію, якщо вона не існує
                    os.makedirs(extension_dir, exist_ok=True)

                    # Генеруємо шлях до файлу призначення
                    dest_file_path = os.path.join(extension_dir, item)

                # Якщо файл не має розширення, копіюємо його в "кореневу директорію"
                # (теку призначення, без піддиректорій)
                else:
                    dest_file_path = os.path.join(dest_dir, item)

                # Передаємо шляхи до вихідного та цільового файлів для копіювання
                copy_file_with_handling(item_path, dest_file_path)

    # Обробляємо будь-які винятки, що виникають під час копіювання
    except Exception as e:
        print(f"Помилка при обробці {source_dir}: {e}")


def copy_file_with_handling(source_file_path: str, dest_file_path: str) -> None:
    """
    Копіює файл з обробкою випадків, коли файл з таким ім'ям вже існує у цільовій директорії.

    Parameters
    ----------
    source_file_path : str
        Шлях до вихідного файлу.
    dest_file_path : str
        Шлях до файлу призначення.
    """
    # Відокремлюємо основну частину імені файлу та його розширення
    base, ext = os.path.splitext(dest_file_path)
    # Початковий суфікс для файлу, що ідентичний за іменем, але має інший вміст
    copy_suffix = "_mod"
    counter = 2
    # Обчислюємо хеш вихідного файлу
    source_file_hash = hash_file_blake2(source_file_path)

    # Перевіряємо, чи існує файл з таким ім'ям у цільовій директорії
    while os.path.exists(dest_file_path):
        # Перевіряємо, чи файли ідентичні за змістом
        if source_file_hash == hash_file_blake2(dest_file_path):
            print(f"Точно такий файл вже скопійовано: {dest_file_path}. Пропускаємо.")
            return

        # Генеруємо нове ім'я з суфіксом
        dest_file_path = f"{base}{copy_suffix}-{counter}{ext}"
        # Підготуємо наступний номер для модифікації файлу
        counter += 1

    # Копіюємо файл за допомогою shutil (забезпечує кросплатформеність)
    try:
        shutil.copy2(source_file_path, dest_file_path)
        print(f"Скопійовано: {source_file_path} -> {dest_file_path}")
    except Exception as e:
        print(f"Помилка при копіюванні {source_file_path} до {dest_file_path}: {e}")


def hash_file_blake2(filename: str) -> str:
    """
    Обчислює хеш BLAKE2 для файлу.

    Parameters
    ----------
    filename : str
        Шлях до файлу.

    Returns
    -------
    str
        Хеш файлу у вигляді рядка.
    """
    # Ініціалізуємо об'єкт хешування BLAKE2
    blake2_hash = hashlib.blake2b()
    try:
        # Відкриваємо файл для читання в бінарному режимі
        with open(filename, "rb") as f:
            # Читаємо файл блоками по 4096 байтів
            for byte_block in iter(lambda: f.read(4096), b""):
                # Оновлюємо хеш для кожного блоку
                blake2_hash.update(byte_block)
        return blake2_hash.hexdigest()
    except Exception as e:
        print(f"Помилка при обчисленні хешу для файлу {filename}: {e}")
        return ""  # Повертаємо порожній рядок у разі помилки


def main() -> None:
    """
    Основна функція для запуску процесу копіювання файлів.

    Перевіряє наявність аргументів командного рядка для вказівки шляхів
    до вихідної та цільової директорій. Запускає процес копіювання файлів
    з вихідної директорії до цільової, створюючи необхідні піддиректорії
    для файлів з розширеннями.

    Parameters
    ----------
    None
    """
    # Перевіряємо наявність двох аргументів командного рядка
    # (шлях до вихідної директорії та директорії призначення)
    if len(sys.argv) < 3:
        print(
            "Використання: 'python3 algo_task_03_1.py <source_directory> <destination_directory>'"
        )
        return  # Завершуємо програму

    # Задаємо вихідну директорію з першого аргументу командного рядка
    source_directory: str = sys.argv[1]
    # Задаємо директорію призначення з другого аргументу
    destination_directory: str = sys.argv[2]

    # Перевіряємо, чи існує вихідна директорія
    if not os.path.exists(source_directory):
        print(f"Вихідна директорія '{source_directory}' не існує.")
        return  # Завершуємо програму

    # Перевіряємо, чи існує директорія призначення, якщо ні - створюємо її
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Запускаємо процес копіювання файлів
    copy_files(source_directory, destination_directory)


if __name__ == "__main__":
    main()

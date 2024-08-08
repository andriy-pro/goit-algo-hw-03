from typing import Dict, List

# Глобальна змінна для підрахунку кроків
step_counter = 0


def move_disks(
    n: int, source: str, target: str, auxiliary: str, rods: Dict[str, List[int]]
) -> None:
    """
    Ханойська вежа: Переміщення дисків з початкового стрижня на цільовий, використовуючи допоміжний стрижень.

    Параметри
    ----------
    n : int
        Кількість дисків для переміщення.
    source : str
        Стрижень, з якого починається переміщення дисків.
    target : str
        Стрижень, на який переміщуються диски.
    auxiliary : str
        Допоміжний стрижень, який використовується у процесі переміщення.
    rods : Dict[str, List[int]]
        Словник, що представляє стан стрижнів.

    """
    global step_counter
    if n == 1:
        # Перемістити один диск безпосередньо з source на target
        disk = rods[source].pop()  # Видаляємо диск з початкового стрижня
        rods[target].append(disk)  # Додаємо диск на цільовий стрижень
        step_counter += 1
        print(f"{step_counter}. Перемістити диск з {source} на {target}: {disk}")
        print(f"\033[1;30mПроміжний стан: {rods}\033[0m")
    else:
        # Перемістити n-1 дисків з source на auxiliary, використовуючи target як допоміжний
        move_disks(n - 1, source, auxiliary, target, rods)

        # Перемістити найбільший диск з source на target
        move_disks(1, source, target, auxiliary, rods)

        # Перемістити n-1 дисків з auxiliary на target, використовуючи source як допоміжний
        move_disks(n - 1, auxiliary, target, source, rods)


def main() -> None:
    """
    Головна функція для виконання рішення задачі Ханойських веж.
    """
    while True:
        try:
            n = int(input("Введіть кількість дисків: "))
            if n <= 0:
                raise ValueError("Кількість дисків має бути додатним числом")
            break
        except ValueError as e:
            print(f"Невірне значення. {e}. Спробуйте ще раз.")

    # Ініціалізуємо початковий стан
    rods = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    print(f"Початковий стан: {rods}")

    # Виконуємо переміщення дисків
    move_disks(n, "A", "C", "B", rods)

    # Виводимо кінцевий стан
    print(f"Кінцевий стан: {rods}")


if __name__ == "__main__":
    main()

import turtle


def koch_snowflake(side_length, level):
    """
    Рекурсивна функція для малювання однієї сторони сніжинки Коха.

    Parameters
    ----------
    side_length : float
        Довжина сторони.
    level : int
        Рівень рекурсії.
    """
    if level == 0:
        turtle.forward(side_length)  # Малюємо пряму лінію для базового випадку
    else:
        side_length /= 3.0  # Ділимо довжину на три частини
        # Рекурсивно малюємо кожну з чотирьох частин кривої Коха
        koch_snowflake(side_length, level - 1)  # Ліва частина
        turtle.left(60)  # Поворот на 60 градусів вліво
        koch_snowflake(side_length, level - 1)  # Середня частина, піднята вгору
        turtle.right(120)  # Поворот на 120 градусів вправо
        koch_snowflake(side_length, level - 1)  # Середня частина, опущена вниз
        turtle.left(60)  # Повертаємося назад на 60 градусів вліво
        koch_snowflake(side_length, level - 1)  # Права частина


def draw_koch_snowflake(side_length, level):
    """
    Функція для малювання сніжинки Коха.

    Parameters
    ----------
    side_length : float
        Довжина сторони.
    level : int
        Рівень рекурсії.
    """
    for _ in range(3):  # Сніжинка складається з трьох кривих Коха
        koch_snowflake(side_length, level)
        turtle.right(120)  # Поворот на 120 градусів для малювання наступної сторони


def main():
    """
    Головна функція для ініціалізації малювання сніжинки Коха з вказаним рівнем рекурсії.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    turtle.setup(width=400, height=400)  # Встановлюємо розмір вікна
    turtle.bgcolor("white")  # Встановлюємо білий фон вікна

    turtle.speed(0)  # Максимальна швидкість малювання
    turtle.color("blue")  # Колір малювання

    side_length = 300  # Задаємо довжину сторони та рівень рекурсії
    level = int(input("Введіть рівень рекурсі (0-5): "))

    # Позиціонуємо черепашку
    turtle.penup()
    turtle.goto(-side_length / 2, side_length / 3)
    turtle.pendown()

    # Запускаємо малювання сніжинки Коха
    draw_koch_snowflake(side_length, level)

    turtle.hideturtle()  # Завершуємо малювання
    turtle.done()  # Завершуємо роботу turtle


if __name__ == "__main__":
    main()

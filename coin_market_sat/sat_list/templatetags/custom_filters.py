from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        # Преобразование строки в Decimal для точности
        value = float(value)
        # Проверка, является ли число целым
        if value > 1:
            return "{:.2f}".format(value)  # Добавление .00 для целых чисел
        else:
            return "{:.6f}".format(value).rstrip('0').rstrip('.')  # Ограничение до 6 знаков после запятой и удаление ненужных нулей
    except (ValueError, TypeError):
        return value  # В случае ошибки возвращаем исходное значение
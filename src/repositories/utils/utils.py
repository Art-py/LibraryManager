def camel_case_to_snake_case(s: str) -> str:
    """Переводит имя класса в наименование таблицы SQL"""
    parts = []
    for char in s:
        if char.isupper():
            parts.append('_')
            parts.append(char.lower())
        else:
            parts.append(char)
    result = ''.join(parts)
    return result.lstrip('_')

def model_to_dict(obj, exclude: set[str] = None) -> dict:
    """Получает модель SQlAlchemy и возвращает словарь полей и значений"""
    exclude = exclude or set()
    return {c.key: getattr(obj, c.key) for c in obj.__mapper__.columns if c.key not in exclude}

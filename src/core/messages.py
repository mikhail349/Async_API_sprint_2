from pydantic import BaseSettings


class MessageSettings(BaseSettings):
    """Настройки сообщений пользователю."""

    FILM_NOT_FOUND: str = 'Кинопроизведение не найдено'
    """Сообщение, если кинопроизведение не найдено."""
    GENRE_NOT_FOUND: str = 'Жанр не найден'
    """Сообщение, если жанр не найден."""
    PERSON_NOT_FOUND: str = 'Персона не найдена'
    """Сообщение, если персона не найдена."""


messages = MessageSettings()

import pygame
from src.engine.services.paths import resource_path


class FontsService:
    """Carga fuentes (.ttf) por tamaño una sola vez."""

    def __init__(self) -> None:
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}

    def get(self, path: str, size: int) -> pygame.font.Font:
        if (path, size) not in self._fonts:
            self._fonts[(path, size)] = pygame.font.Font(
                resource_path(path), size)
        return self._fonts[(path, size)]

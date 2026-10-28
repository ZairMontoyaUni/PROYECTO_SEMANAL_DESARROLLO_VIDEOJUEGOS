import pygame
from src.engine.services.paths import resource_path


class SoundsService:
    """Carga sonidos una sola vez y permite reproducirlos."""

    def __init__(self) -> None:
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def get(self, path: str) -> pygame.mixer.Sound | None:
        if pygame.mixer.get_init() is None:
            return None  # el equipo no tiene audio disponible
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(resource_path(path))
        return self._sounds[path]

    def play(self, path: str) -> None:
        sound = self.get(path)
        if sound is not None:
            sound.play()

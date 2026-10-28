import pygame
from src.engine.services.paths import resource_path


class ImagesService:
    """Carga imágenes una sola vez y las guarda en caché."""

    def __init__(self) -> None:
        self._images: dict[str, pygame.Surface] = {}

    def get(self, path: str) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(
                resource_path(path)).convert_alpha()
        return self._images[path]

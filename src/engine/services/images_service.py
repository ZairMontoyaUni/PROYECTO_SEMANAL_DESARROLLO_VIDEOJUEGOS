import pathlib
import pygame

ROOT_PATH = pathlib.Path(__file__).resolve().parents[3]
_images: dict[str, pygame.Surface] = {}


def get_image(path: str) -> pygame.Surface:
    """Carga una imagen (ruta relativa a main.py) y la guarda en caché."""
    if path not in _images:
        _images[path] = pygame.image.load(ROOT_PATH / path).convert_alpha()
    return _images[path]

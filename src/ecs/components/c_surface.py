import pygame


class CSurface:
    """Textura de una entidad y el área (cuadro) que se dibuja de ella."""

    def __init__(self, surf: pygame.Surface, number_frames: int = 1) -> None:
        self.surf = surf
        self.area = pygame.Rect(0, 0, surf.get_width() // number_frames,
                                surf.get_height())

    def get_rect(self, pos: pygame.Vector2) -> pygame.Rect:
        """Rectángulo que ocupa la entidad en pantalla (para colisiones)."""
        return pygame.Rect(pos, self.area.size)

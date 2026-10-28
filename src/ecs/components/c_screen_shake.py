import pygame


class CScreenShake:
    """Temblor de pantalla (game feel) al usar el ataque especial."""

    def __init__(self, duration: float, intensity: int) -> None:
        self.duration = duration
        self.intensity = intensity
        self.time_left = 0.0
        self.offset = pygame.Vector2()

    def start(self) -> None:
        self.time_left = self.duration

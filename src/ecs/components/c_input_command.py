from enum import Enum
import pygame


class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2


class CInputCommand:
    """Asocia un nombre de acción con una tecla o botón del ratón."""

    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        self.pos = pygame.Vector2()  # posición del ratón (PLAYER_FIRE)

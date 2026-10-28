from enum import Enum
import pygame


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2


class CHunterState:
    """Estado y parámetros del enemigo Hunter."""

    def __init__(self, origin: pygame.Vector2, enemy_info: dict) -> None:
        self.state = HunterState.IDLE
        self.origin = pygame.Vector2(origin)
        self.velocity_chase = enemy_info["velocity_chase"]
        self.velocity_return = enemy_info["velocity_return"]
        self.distance_start_chase = enemy_info["distance_start_chase"]
        self.distance_start_return = enemy_info["distance_start_return"]
        self.sound_chase = enemy_info["sound_chase"]

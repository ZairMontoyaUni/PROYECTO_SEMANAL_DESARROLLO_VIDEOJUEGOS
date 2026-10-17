import pygame


class CVelocity:
    def __init__(self, vel: pygame.Vector2 | None = None) -> None:
        self.vel = vel if vel is not None else pygame.Vector2()

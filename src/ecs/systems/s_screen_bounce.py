import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity


def system_screen_bounce(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface, CVelocity)
    screen_rect = screen.get_rect()

    c_t: CTransform
    c_s: CSurface
    c_v: CVelocity
    for _entity, (c_t, c_s, c_v) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left <= 0 or cuad_rect.right >= screen_rect.width:
            c_v.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.x = cuad_rect.x
        if cuad_rect.top <= 0 or cuad_rect.bottom >= screen_rect.height:
            c_v.vel.y *= -1
            c_t.pos.y = cuad_rect.y

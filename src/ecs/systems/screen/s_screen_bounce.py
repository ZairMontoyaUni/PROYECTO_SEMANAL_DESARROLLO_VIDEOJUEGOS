import esper
import pygame
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_velocity import CVelocity


def system_screen_bounce(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface, CVelocity,
                                      CTagEnemy)
    screen_rect = screen.get_rect()

    c_t: CTransform
    c_s: CSurface
    c_v: CVelocity
    for entity, (c_t, c_s, c_v, _tag) in components:
        if world.has_component(entity, CHunterState):
            continue  # los Hunter no rebotan: se mueven según su estado
        cuad_rect = c_s.get_rect(c_t.pos)
        if ((cuad_rect.left <= 0 and c_v.vel.x < 0) or
                (cuad_rect.right >= screen_rect.width and c_v.vel.x > 0)):
            c_v.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.x = cuad_rect.x
        if ((cuad_rect.top <= 0 and c_v.vel.y < 0) or
                (cuad_rect.bottom >= screen_rect.height and c_v.vel.y > 0)):
            c_v.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.y = cuad_rect.y

import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform


def system_screen_bullet(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface, CTagBullet)
    screen_rect = screen.get_rect()

    c_t: CTransform
    c_s: CSurface
    for entity, (c_t, c_s, _tag) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not screen_rect.contains(bullet_rect):
            world.delete_entity(entity, immediate=True)

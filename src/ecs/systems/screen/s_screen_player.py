import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def system_screen_player(world: esper.World, screen: pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface, CTagPlayer)
    screen_rect = screen.get_rect()

    c_t: CTransform
    c_s: CSurface
    for _entity, (c_t, c_s, _tag) in components:
        player_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if not screen_rect.contains(player_rect):
            player_rect.clamp_ip(screen_rect)
            c_t.pos.x = player_rect.x
            c_t.pos.y = player_rect.y

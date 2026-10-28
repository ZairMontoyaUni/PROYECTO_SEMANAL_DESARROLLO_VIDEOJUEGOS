import esper
import pygame
from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_hud import CTagHud


def system_rendering(world: esper.World, screen: pygame.Surface) -> None:
    shake = pygame.Vector2()
    for _entity, c_shake in world.get_component(CScreenShake):
        shake = c_shake.offset

    c_t: CTransform
    c_s: CSurface
    # Primero el juego (con el temblor de pantalla)...
    for entity, (c_t, c_s) in world.get_components(CTransform, CSurface):
        if not world.has_component(entity, CTagHud):
            screen.blit(c_s.surf, c_t.pos + shake, c_s.area)
    # ...y encima los textos de la interfaz, que no tiemblan.
    for _entity, (c_t, c_s, _tag) in world.get_components(CTransform, CSurface,
                                                          CTagHud):
        screen.blit(c_s.surf, c_t.pos, c_s.area)

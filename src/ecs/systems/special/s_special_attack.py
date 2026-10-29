import esper
import pygame
from src.create.prefab_creator import crear_bala_especial
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet
from src.engine.service_locator import ServiceLocator


def system_special_attack(world: esper.World, special_info: dict) -> bool:
    """Divide cada bala en vuelo en 4 balas que salen en sus diagonales.

    Devuelve True si había al menos una bala para dividir.
    """
    bullets = world.get_components(CTransform, CSurface, CVelocity, CTagBullet)

    divided = False
    for entity, (c_t, c_s, c_v, _tag) in bullets:
        if world.has_component(entity, CTagSpecialBullet):
            continue  # las balas del especial no se vuelven a dividir
        center = c_t.pos + pygame.Vector2(c_s.area.size) / 2
        for angle in (45, 135, 225, 315):
            crear_bala_especial(world, center, c_v.vel.rotate(angle),
                                special_info)
        world.delete_entity(entity, immediate=True)
        divided = True

    if divided:
        ServiceLocator.sounds_service.play(special_info["sound"])  # una vez
    return divided

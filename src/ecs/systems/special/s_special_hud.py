import esper
import pygame
from src.ecs.components.c_special_ability import CSpecialAbility
from src.ecs.components.c_special_hud import CSpecialHud
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_special_hud(world: esper.World) -> None:
    abilities = world.get_component(CSpecialAbility)
    if not abilities:
        return
    _player_entity, c_sa = abilities[0]

    c_hud: CSpecialHud
    c_s: CSurface
    for _entity, (c_hud, c_s) in world.get_components(CSpecialHud, CSurface):
        if c_sa.time_left <= 0:
            info = c_hud.ready_info
            text = info["text"]
        else:
            info = c_hud.cooldown_info
            text = info["text"].format(seconds=f"{c_sa.time_left:.1f}")
        if text != c_hud.last_text:  # solo se vuelve a dibujar si cambió
            c_hud.last_text = text
            font = ServiceLocator.fonts_service.get(info["font"],
                                                    info["size"])
            color = pygame.Color(info["color"]["r"], info["color"]["g"],
                                 info["color"]["b"])
            new_surface = CSurface.from_text(text, font, color)
            c_s.surf = new_surface.surf
            c_s.area = new_surface.area

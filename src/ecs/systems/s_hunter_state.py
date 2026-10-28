import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def system_hunter_state(world: esper.World, delta_time: float) -> None:
    players = world.get_components(CTransform, CSurface, CTagPlayer)
    if not players:
        return
    _player_entity, (c_t_p, c_s_p, _tag) = players[0]
    player_center = c_t_p.pos + pygame.Vector2(c_s_p.area.size) / 2

    hunters = world.get_components(CTransform, CVelocity, CSurface,
                                   CAnimation, CHunterState)
    c_t: CTransform
    c_v: CVelocity
    c_s: CSurface
    c_a: CAnimation
    c_h: CHunterState
    for _entity, (c_t, c_v, c_s, c_a, c_h) in hunters:
        hunter_center = c_t.pos + pygame.Vector2(c_s.area.size) / 2

        # Cambios de estado
        if (c_h.state == HunterState.IDLE and
                hunter_center.distance_to(player_center)
                <= c_h.distance_start_chase):
            c_h.state = HunterState.CHASE
            ServiceLocator.sounds_service.play(c_h.sound_chase)
        elif (c_h.state == HunterState.CHASE and
              c_t.pos.distance_to(c_h.origin) >= c_h.distance_start_return):
            c_h.state = HunterState.RETURN

        # Comportamiento de cada estado
        if c_h.state == HunterState.IDLE:
            c_v.vel.update(0, 0)
        elif c_h.state == HunterState.CHASE:
            _mover_hacia(c_v, player_center - hunter_center,
                         c_h.velocity_chase)
        elif c_h.state == HunterState.RETURN:
            to_origin = c_h.origin - c_t.pos
            if to_origin.length() <= c_h.velocity_return * delta_time:
                c_t.pos = pygame.Vector2(c_h.origin)  # llegó a su origen
                c_v.vel.update(0, 0)
                c_h.state = HunterState.IDLE
            else:
                _mover_hacia(c_v, to_origin, c_h.velocity_return)

        c_a.set_animation("MOVE" if c_v.vel.length() > 0 else "IDLE")


def _mover_hacia(c_v: CVelocity, direction: pygame.Vector2,
                 speed: float) -> None:
    if direction.length() == 0:
        c_v.vel.update(0, 0)
    else:
        c_v.vel = direction.normalize() * speed

import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_animation_state(world: esper.World) -> None:
    components = world.get_components(CVelocity, CAnimation, CTagPlayer)

    c_v: CVelocity
    c_a: CAnimation
    for _entity, (c_v, c_a, _tag) in components:
        c_a.set_animation("MOVE" if c_v.vel.length() > 0 else "IDLE")

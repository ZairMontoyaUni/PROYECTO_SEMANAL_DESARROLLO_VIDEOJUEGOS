import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_end(world: esper.World) -> None:
    components = world.get_components(CAnimation, CTagExplosion)

    c_a: CAnimation
    for entity, (c_a, _tag) in components:
        if c_a.finished:
            world.delete_entity(entity, immediate=True)

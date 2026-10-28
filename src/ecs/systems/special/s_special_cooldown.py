import esper
from src.ecs.components.c_special_ability import CSpecialAbility


def system_special_cooldown(world: esper.World, delta_time: float) -> None:
    c_sa: CSpecialAbility
    for _entity, c_sa in world.get_component(CSpecialAbility):
        c_sa.time_left = max(0.0, c_sa.time_left - delta_time)

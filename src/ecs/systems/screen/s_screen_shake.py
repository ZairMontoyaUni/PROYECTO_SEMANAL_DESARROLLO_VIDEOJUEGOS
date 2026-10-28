import random
import esper
from src.ecs.components.c_screen_shake import CScreenShake


def system_screen_shake(world: esper.World, delta_time: float) -> None:
    c_shake: CScreenShake
    for _entity, c_shake in world.get_component(CScreenShake):
        if c_shake.time_left > 0:
            c_shake.time_left -= delta_time
            c_shake.offset.update(
                random.randint(-c_shake.intensity, c_shake.intensity),
                random.randint(-c_shake.intensity, c_shake.intensity))
        else:
            c_shake.offset.update(0, 0)
        if c_shake.time_left <= 0:
            c_shake.offset.update(0, 0)

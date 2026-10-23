import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float) -> None:
    components = world.get_components(CAnimation, CSurface)

    c_a: CAnimation
    c_s: CSurface
    for _entity, (c_a, c_s) in components:
        anim = c_a.animations[c_a.curr_anim]
        frame_duration = 1.0 / anim.framerate
        c_a.curr_anim_time += delta_time
        while c_a.curr_anim_time >= frame_duration:
            c_a.curr_anim_time -= frame_duration
            c_a.curr_frame += 1
            if c_a.curr_frame > anim.end:
                c_a.curr_frame = anim.start
                c_a.finished = True
        c_s.area.x = c_s.area.w * c_a.curr_frame

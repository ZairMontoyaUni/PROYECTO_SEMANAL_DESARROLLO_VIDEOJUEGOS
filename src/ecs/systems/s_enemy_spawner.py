import esper
from src.create.prefab_creator import crear_enemigo
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(world: esper.World, enemies_data: dict,
                         delta_time: float) -> None:
    components = world.get_component(CEnemySpawner)

    c_spw: CEnemySpawner
    for _entity, c_spw in components:
        c_spw.elapsed_time += delta_time
        for event in c_spw.spawn_events:
            if not event.triggered and c_spw.elapsed_time >= event.time:
                event.triggered = True
                crear_enemigo(world, event.pos, enemies_data[event.enemy_type])

import esper
import pygame
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_collision_player_enemy(world: esper.World,
                                  player_spawn: dict) -> None:
    players = world.get_components(CTransform, CSurface, CTagPlayer)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for _player_entity, (c_t_p, c_s_p, _tag_p) in players:
        player_rect = c_s_p.surf.get_rect(topleft=c_t_p.pos)
        for _enemy_entity, (c_t_e, c_s_e, _tag_e) in enemies:
            enemy_rect = c_s_e.surf.get_rect(topleft=c_t_e.pos)
            if player_rect.colliderect(enemy_rect):
                _morir(world, c_t_p, c_s_p, player_spawn)
                return


def _morir(world: esper.World, c_t_p: CTransform, c_s_p: CSurface,
           player_spawn: dict) -> None:
    # 1. El jugador vuelve a su posición de origen (centrado en ese punto).
    center = pygame.Vector2(player_spawn["position"]["x"],
                            player_spawn["position"]["y"])
    c_t_p.pos = center - pygame.Vector2(c_s_p.surf.get_size()) / 2

    # 2. Desaparecen todos los enemigos que existan.
    for enemy_entity, _tag in world.get_component(CTagEnemy):
        world.delete_entity(enemy_entity, immediate=True)

    # 3. El nivel se reinicia: todos los enemigos podrán volver a aparecer.
    c_spw: CEnemySpawner
    for _entity, c_spw in world.get_component(CEnemySpawner):
        c_spw.elapsed_time = 0.0
        for event in c_spw.spawn_events:
            event.triggered = False

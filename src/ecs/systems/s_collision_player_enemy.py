import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def system_collision_player_enemy(world: esper.World) -> None:
    players = world.get_components(CTransform, CSurface, CTagPlayer)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for _player_entity, (c_t_p, c_s_p, _tag_p) in players:
        player_rect = c_s_p.surf.get_rect(topleft=c_t_p.pos)
        for enemy_entity, (c_t_e, c_s_e, _tag_e) in enemies:
            enemy_rect = c_s_e.surf.get_rect(topleft=c_t_e.pos)
            if player_rect.colliderect(enemy_rect):
                world.delete_entity(enemy_entity, immediate=True)

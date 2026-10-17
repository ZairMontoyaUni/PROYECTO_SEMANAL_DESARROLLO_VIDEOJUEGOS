import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_transform import CTransform


def system_collision_enemy_bullet(world: esper.World) -> None:
    bullets = world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_t_b, c_s_b, _tag_b) in bullets:
        bullet_rect = c_s_b.surf.get_rect(topleft=c_t_b.pos)
        # Se vuelve a pedir la lista de enemigos por cada bala para no
        # usar enemigos que ya fueron eliminados.
        enemies = world.get_components(CTransform, CSurface, CTagEnemy)
        for enemy_entity, (c_t_e, c_s_e, _tag_e) in enemies:
            enemy_rect = c_s_e.surf.get_rect(topleft=c_t_e.pos)
            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity, immediate=True)
                world.delete_entity(enemy_entity, immediate=True)
                break

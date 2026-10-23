import esper
import pygame
from src.create.prefab_creator import crear_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_enemy_bullet(world: esper.World,
                                  explosion_info: dict) -> None:
    bullets = world.get_components(CTransform, CSurface, CTagBullet)

    for bullet_entity, (c_t_b, c_s_b, _tag_b) in bullets:
        bullet_rect = c_s_b.get_rect(c_t_b.pos)
        # Se vuelve a pedir la lista de enemigos por cada bala para no
        # usar enemigos que ya fueron eliminados.
        enemies = world.get_components(CTransform, CSurface, CTagEnemy)
        for enemy_entity, (c_t_e, c_s_e, _tag_e) in enemies:
            enemy_rect = c_s_e.get_rect(c_t_e.pos)
            if bullet_rect.colliderect(enemy_rect):
                crear_explosion(world, pygame.Vector2(enemy_rect.center),
                                explosion_info)
                world.delete_entity(bullet_entity, immediate=True)
                world.delete_entity(enemy_entity, immediate=True)
                break

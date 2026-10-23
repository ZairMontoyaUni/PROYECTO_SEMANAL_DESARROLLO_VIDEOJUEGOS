import random
import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.services.images_service import get_image


def crear_sprite(world: esper.World, pos: pygame.Vector2,
                 vel: pygame.Vector2, info: dict) -> int:
    """Crea una entidad con textura (y animaciones si el cfg las trae)."""
    entity = world.create_entity()
    animations = info.get("animations")
    number_frames = animations["number_frames"] if animations else 1
    world.add_component(entity, CSurface(get_image(info["image"]),
                                         number_frames))
    world.add_component(entity, CTransform(pos=pos))
    world.add_component(entity, CVelocity(vel=vel))
    if animations:
        world.add_component(entity, CAnimation(animations))
    return entity


def _centrar(world: esper.World, entity: int, center: pygame.Vector2) -> None:
    c_t = world.component_for_entity(entity, CTransform)
    c_s = world.component_for_entity(entity, CSurface)
    c_t.pos = center - pygame.Vector2(c_s.area.size) / 2


def crear_enemigo(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    if "velocity_chase" in enemy_info:  # Hunter: se mueve según su estado
        enemy_entity = crear_sprite(world, pygame.Vector2(pos),
                                    pygame.Vector2(), enemy_info)
        world.add_component(enemy_entity, CHunterState(pos, enemy_info))
    else:  # Asteroide: rebota por la pantalla
        speed = random.uniform(enemy_info["velocity_min"],
                               enemy_info["velocity_max"])
        vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
        enemy_entity = crear_sprite(world, pygame.Vector2(pos), vel,
                                    enemy_info)
    world.add_component(enemy_entity, CTagEnemy())


def crear_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data))


def crear_jugador(world: esper.World, player_info: dict,
                  spawn_info: dict) -> int:
    player_entity = crear_sprite(world, pygame.Vector2(), pygame.Vector2(),
                                 player_info)
    _centrar(world, player_entity,
             pygame.Vector2(spawn_info["position"]["x"],
                            spawn_info["position"]["y"]))
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def crear_bala(world: esper.World, origin: pygame.Vector2,
               target: pygame.Vector2, bullet_info: dict) -> None:
    direction = target - origin
    if direction.length() == 0:
        return  # el clic fue justo en el centro del jugador: no hay dirección
    vel = direction.normalize() * bullet_info["velocity"]
    bullet_entity = crear_sprite(world, pygame.Vector2(), vel, bullet_info)
    _centrar(world, bullet_entity, origin)
    world.add_component(bullet_entity, CTagBullet())


def crear_explosion(world: esper.World, center: pygame.Vector2,
                    explosion_info: dict) -> None:
    explosion_entity = crear_sprite(world, pygame.Vector2(),
                                    pygame.Vector2(), explosion_info)
    _centrar(world, explosion_entity, center)
    world.add_component(explosion_entity, CTagExplosion())


def crear_input_player(world: esper.World) -> None:
    acciones = {
        "PLAYER_LEFT": pygame.K_LEFT,
        "PLAYER_RIGHT": pygame.K_RIGHT,
        "PLAYER_UP": pygame.K_UP,
        "PLAYER_DOWN": pygame.K_DOWN,
        "PLAYER_FIRE": pygame.BUTTON_LEFT,
    }
    for nombre, tecla in acciones.items():
        input_entity = world.create_entity()
        world.add_component(input_entity, CInputCommand(nombre, tecla))

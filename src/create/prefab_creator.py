import random
import esper
import pygame
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def crear_cuadrado(world: esper.World, pos: pygame.Vector2,
                   size: pygame.Vector2, color: pygame.Color,
                   vel: pygame.Vector2) -> int:
    cuadrado_entity = world.create_entity()
    world.add_component(cuadrado_entity, CSurface(size=size, color=color))
    world.add_component(cuadrado_entity, CTransform(pos=pos))
    world.add_component(cuadrado_entity, CVelocity(vel=vel))
    return cuadrado_entity


def crear_enemigo(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    size = pygame.Vector2(enemy_info["size"]["x"], enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    speed = random.uniform(enemy_info["velocity_min"],
                           enemy_info["velocity_max"])
    vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    enemy_entity = crear_cuadrado(world, pygame.Vector2(pos), size, color, vel)
    world.add_component(enemy_entity, CTagEnemy())


def crear_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data))


def crear_jugador(world: esper.World, player_info: dict,
                  spawn_info: dict) -> int:
    size = pygame.Vector2(player_info["size"]["x"], player_info["size"]["y"])
    color = pygame.Color(player_info["color"]["r"],
                         player_info["color"]["g"],
                         player_info["color"]["b"])
    center = pygame.Vector2(spawn_info["position"]["x"],
                            spawn_info["position"]["y"])
    pos = center - size / 2  # el jugador queda centrado en el punto de origen
    player_entity = crear_cuadrado(world, pos, size, color, pygame.Vector2())
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def crear_bala(world: esper.World, origin: pygame.Vector2,
               target: pygame.Vector2, bullet_info: dict) -> None:
    direction = target - origin
    if direction.length() == 0:
        return  # el clic fue justo en el centro del jugador: no hay dirección
    size = pygame.Vector2(bullet_info["size"]["x"], bullet_info["size"]["y"])
    color = pygame.Color(bullet_info["color"]["r"],
                         bullet_info["color"]["g"],
                         bullet_info["color"]["b"])
    vel = direction.normalize() * bullet_info["velocity"]
    pos = origin - size / 2  # el centro de la bala sale del centro del jugador
    bullet_entity = crear_cuadrado(world, pos, size, color, vel)
    world.add_component(bullet_entity, CTagBullet())


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

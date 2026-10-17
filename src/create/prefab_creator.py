import random
import esper
import pygame
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def crear_cuadrado(world: esper.World, pos: pygame.Vector2,
                   size: pygame.Vector2, color: pygame.Color,
                   vel: pygame.Vector2):
    cuadrado_entity = world.create_entity()
    world.add_component(cuadrado_entity, CSurface(size=size, color=color))
    world.add_component(cuadrado_entity, CTransform(pos=pos))
    world.add_component(cuadrado_entity, CVelocity(vel=vel))


def crear_enemigo(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    size = pygame.Vector2(enemy_info["size"]["x"], enemy_info["size"]["y"])
    color = pygame.Color(enemy_info["color"]["r"],
                         enemy_info["color"]["g"],
                         enemy_info["color"]["b"])
    speed = random.uniform(enemy_info["velocity_min"],
                           enemy_info["velocity_max"])
    vel = pygame.Vector2(speed, 0).rotate(random.uniform(0, 360))
    crear_cuadrado(world, pygame.Vector2(pos), size, color, vel)


def crear_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data))

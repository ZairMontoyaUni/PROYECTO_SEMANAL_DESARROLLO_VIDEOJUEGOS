import random
import esper
import pygame
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_special_ability import CSpecialAbility
from src.ecs.components.c_special_hud import CSpecialHud
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hud import CTagHud
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet
from src.engine.service_locator import ServiceLocator


def crear_sprite(world: esper.World, pos: pygame.Vector2,
                 vel: pygame.Vector2, info: dict,
                 play_sound: bool = True) -> int:
    """Crea una entidad con textura (y animaciones si el cfg las trae)."""
    entity = world.create_entity()
    if play_sound and "sound" in info:
        ServiceLocator.sounds_service.play(info["sound"])
    animations = info.get("animations")
    number_frames = animations["number_frames"] if animations else 1
    world.add_component(entity, CSurface(
        ServiceLocator.images_service.get(info["image"]), number_frames))
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
                  spawn_info: dict, special_info: dict) -> int:
    player_entity = crear_sprite(world, pygame.Vector2(), pygame.Vector2(),
                                 player_info)
    _centrar(world, player_entity,
             pygame.Vector2(spawn_info["position"]["x"],
                            spawn_info["position"]["y"]))
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity,
                        CSpecialAbility(special_info["cooldown"]))
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


def crear_bala_especial(world: esper.World, center: pygame.Vector2,
                        direction: pygame.Vector2, special_info: dict) -> None:
    """Crea una bala especial en 'center' que viaja hacia 'direction'."""
    vel = direction.normalize() * special_info["velocity"]
    bullet_entity = crear_sprite(world, pygame.Vector2(), vel, special_info,
                                 play_sound=False)
    _centrar(world, bullet_entity, center)
    world.add_component(bullet_entity, CTagBullet())
    world.add_component(bullet_entity, CTagSpecialBullet())


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
        "PLAYER_SPECIAL": pygame.BUTTON_RIGHT,
        "PAUSE_GAME": pygame.K_p,
    }
    for nombre, tecla in acciones.items():
        input_entity = world.create_entity()
        world.add_component(input_entity, CInputCommand(nombre, tecla))


def crear_texto(world: esper.World, text_info: dict) -> int:
    """Crea un texto fijo de la interfaz a partir de su cfg."""
    font = ServiceLocator.fonts_service.get(text_info["font"],
                                            text_info["size"])
    color = pygame.Color(text_info["color"]["r"], text_info["color"]["g"],
                         text_info["color"]["b"])
    c_s = CSurface.from_text(text_info["text"], font, color)
    pos = pygame.Vector2(text_info["position"]["x"],
                         text_info["position"]["y"])
    if text_info["anchor"] == "center":
        pos -= pygame.Vector2(c_s.area.size) / 2
    text_entity = world.create_entity()
    world.add_component(text_entity, c_s)
    world.add_component(text_entity, CTransform(pos=pos))
    world.add_component(text_entity, CTagHud())
    return text_entity


def crear_texto_pausa(world: esper.World, pause_info: dict) -> None:
    pause_entity = crear_texto(world, pause_info)
    world.add_component(pause_entity, CTagPause())


def crear_hud_especial(world: esper.World, interface_info: dict) -> None:
    hud_entity = crear_texto(world, interface_info["special_ready"])
    hud = CSpecialHud(interface_info["special_ready"],
                      interface_info["special_cooldown"])
    hud.last_text = interface_info["special_ready"]["text"]
    world.add_component(hud_entity, hud)


def crear_screen_shake(world: esper.World, special_info: dict) -> int:
    shake_entity = world.create_entity()
    world.add_component(shake_entity,
                        CScreenShake(special_info["shake"]["duration"],
                                     special_info["shake"]["intensity"]))
    return shake_entity

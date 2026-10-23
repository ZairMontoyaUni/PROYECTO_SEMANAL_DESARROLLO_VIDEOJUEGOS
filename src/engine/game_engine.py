import json
import pathlib
import esper
import pygame
from src.create.prefab_creator import (crear_bala, crear_enemy_spawner,
                                       crear_input_player, crear_jugador)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.animation.s_animation import system_animation
from src.ecs.systems.animation.s_explosion_end import system_explosion_end
from src.ecs.systems.animation.s_player_animation_state import (
    system_player_animation_state)
from src.ecs.systems.collision.s_collision_enemy_bullet import (
    system_collision_enemy_bullet)
from src.ecs.systems.collision.s_collision_player_enemy import (
    system_collision_player_enemy)
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.screen.s_screen_bounce import system_screen_bounce
from src.ecs.systems.screen.s_screen_bullet import system_screen_bullet
from src.ecs.systems.screen.s_screen_player import system_screen_player

CFG_PATH = pathlib.Path(__file__).resolve().parents[2] / "assets" / "cfg"


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        self.window_size = (self.window_cfg["size"]["w"],
                            self.window_cfg["size"]["h"])
        self.screen = pygame.display.set_mode(self.window_size,
                                              pygame.RESIZABLE)
        pygame.display.set_caption(self.window_cfg["title"])

        self.is_fullscreen = False
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = self.window_cfg["framerate"]
        self.delta_time = 0.0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

    def _load_config_files(self) -> None:
        with open(CFG_PATH / "window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open(CFG_PATH / "enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open(CFG_PATH / "level_01.json", encoding="utf-8") as level_file:
            self.level_01_cfg = json.load(level_file)
        with open(CFG_PATH / "player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open(CFG_PATH / "bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open(CFG_PATH / "explosion.json",
                  encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        crear_enemy_spawner(self.ecs_world, self.level_01_cfg)
        self._player_entity = crear_jugador(self.ecs_world, self.player_cfg,
                                            self.level_01_cfg["player_spawn"])
        self._player_c_t = self.ecs_world.component_for_entity(
            self._player_entity, CTransform)
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(
            self._player_entity, CSurface)
        crear_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self._toggle_fullscreen()
            system_input_player(self.ecs_world, event, self._do_action)

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.window_size,
                                                  pygame.RESIZABLE)

    def _do_action(self, c_input: CInputCommand):
        speed = self.player_cfg["input_velocity"]
        vel = self._player_c_v.vel
        if c_input.name == "PLAYER_LEFT":
            vel.x += -speed if c_input.phase == CommandPhase.START else speed
        elif c_input.name == "PLAYER_RIGHT":
            vel.x += speed if c_input.phase == CommandPhase.START else -speed
        elif c_input.name == "PLAYER_UP":
            vel.y += -speed if c_input.phase == CommandPhase.START else speed
        elif c_input.name == "PLAYER_DOWN":
            vel.y += speed if c_input.phase == CommandPhase.START else -speed
        elif c_input.name == "PLAYER_FIRE":
            max_bullets = self.level_01_cfg["player_spawn"]["max_bullets"]
            if len(self.ecs_world.get_component(CTagBullet)) < max_bullets:
                player_size = pygame.Vector2(self._player_c_s.area.size)
                player_center = self._player_c_t.pos + player_size / 2
                crear_bala(self.ecs_world, player_center, c_input.pos,
                           self.bullet_cfg)

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_hunter_state(self.ecs_world, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(self.ecs_world, self.screen)
        system_collision_enemy_bullet(self.ecs_world, self.explosion_cfg)
        system_collision_player_enemy(self.ecs_world,
                                      self.level_01_cfg["player_spawn"],
                                      self.explosion_cfg)
        system_screen_bullet(self.ecs_world, self.screen)
        system_player_animation_state(self.ecs_world)
        system_animation(self.ecs_world, self.delta_time)
        system_explosion_end(self.ecs_world)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

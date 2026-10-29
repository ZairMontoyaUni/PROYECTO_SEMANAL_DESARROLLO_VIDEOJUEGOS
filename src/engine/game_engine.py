import asyncio
import esper
import pygame
from src.create.prefab_creator import (crear_bala, crear_enemy_spawner,
                                       crear_hud_especial,
                                       crear_input_player, crear_jugador,
                                       crear_screen_shake, crear_texto,
                                       crear_texto_pausa)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_screen_shake import CScreenShake
from src.ecs.components.c_special_ability import CSpecialAbility
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_pause import CTagPause
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet
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
from src.ecs.systems.screen.s_screen_shake import system_screen_shake
from src.ecs.systems.special.s_special_attack import system_special_attack
from src.ecs.systems.special.s_special_cooldown import system_special_cooldown
from src.ecs.systems.special.s_special_hud import system_special_hud
from src.engine.service_locator import ServiceLocator

CFG_FILES = "assets/cfg/"


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
        self.is_paused = False
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.frame_rate = self.window_cfg["framerate"]
        self.delta_time = 0.0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

    def _load_config_files(self) -> None:
        configs = ServiceLocator.configs_service
        self.window_cfg = configs.get(CFG_FILES + "window.json")
        self.enemies_cfg = configs.get(CFG_FILES + "enemies.json")
        self.level_01_cfg = configs.get(CFG_FILES + "level_01.json")
        self.player_cfg = configs.get(CFG_FILES + "player.json")
        self.bullet_cfg = configs.get(CFG_FILES + "bullet.json")
        self.explosion_cfg = configs.get(CFG_FILES + "explosion.json")
        self.special_cfg = configs.get(CFG_FILES + "special.json")
        self.interface_cfg = configs.get(CFG_FILES + "interface.json")

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            if not self.is_paused:
                self._update()
            self._draw()
            await asyncio.sleep(0)  # necesario para la versión web (pygbag)
        self._clean()

    def _create(self):
        crear_enemy_spawner(self.ecs_world, self.level_01_cfg)
        self._player_entity = crear_jugador(self.ecs_world, self.player_cfg,
                                            self.level_01_cfg["player_spawn"],
                                            self.special_cfg)
        self._player_c_t = self.ecs_world.component_for_entity(
            self._player_entity, CTransform)
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity)
        self._player_c_s = self.ecs_world.component_for_entity(
            self._player_entity, CSurface)
        self._player_c_sa = self.ecs_world.component_for_entity(
            self._player_entity, CSpecialAbility)
        self._screen_shake = self.ecs_world.component_for_entity(
            crear_screen_shake(self.ecs_world, self.special_cfg),
            CScreenShake)
        crear_input_player(self.ecs_world)
        crear_texto(self.ecs_world, self.interface_cfg["title"])
        crear_texto(self.ecs_world, self.interface_cfg["instructions"])
        crear_hud_especial(self.ecs_world, self.interface_cfg)

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

    def _toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            crear_texto_pausa(self.ecs_world, self.interface_cfg["pause"])
        else:
            for entity, _tag in self.ecs_world.get_component(CTagPause):
                self.ecs_world.delete_entity(entity, immediate=True)

    def _do_action(self, c_input: CInputCommand):
        speed = self.player_cfg["input_velocity"]
        vel = self._player_c_v.vel
        # El movimiento se acumula también en pausa para no perder teclas
        # que se suelten mientras el juego está detenido.
        if c_input.name == "PLAYER_LEFT":
            vel.x += -speed if c_input.phase == CommandPhase.START else speed
        elif c_input.name == "PLAYER_RIGHT":
            vel.x += speed if c_input.phase == CommandPhase.START else -speed
        elif c_input.name == "PLAYER_UP":
            vel.y += -speed if c_input.phase == CommandPhase.START else speed
        elif c_input.name == "PLAYER_DOWN":
            vel.y += speed if c_input.phase == CommandPhase.START else -speed
        elif c_input.name == "PAUSE_GAME":
            if c_input.phase == CommandPhase.START:  # solo al presionar
                self._toggle_pause()
        elif self.is_paused:
            return  # en pausa no se puede disparar
        elif c_input.name == "PLAYER_FIRE":
            self._fire_bullet(c_input)
        elif c_input.name == "PLAYER_SPECIAL":
            self._fire_special()

    def _player_center(self) -> pygame.Vector2:
        player_size = pygame.Vector2(self._player_c_s.area.size)
        return self._player_c_t.pos + player_size / 2

    def _fire_bullet(self, c_input: CInputCommand):
        max_bullets = self.level_01_cfg["player_spawn"]["max_bullets"]
        # Las balas del ataque especial no cuentan para el límite.
        current = (len(self.ecs_world.get_component(CTagBullet))
                   - len(self.ecs_world.get_component(CTagSpecialBullet)))
        if current < max_bullets:
            crear_bala(self.ecs_world, self._player_center(), c_input.pos,
                       self.bullet_cfg)

    def _fire_special(self):
        if self._player_c_sa.time_left > 0:
            return  # todavía recargando
        if system_special_attack(self.ecs_world, self.special_cfg):
            self._player_c_sa.time_left = self._player_c_sa.cooldown
            self._screen_shake.start()

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
        system_special_cooldown(self.ecs_world, self.delta_time)
        system_special_hud(self.ecs_world)
        system_screen_shake(self.ecs_world, self.delta_time)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

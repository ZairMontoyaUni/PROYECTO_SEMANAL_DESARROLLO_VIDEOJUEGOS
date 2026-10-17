import json
import pathlib
import esper
import pygame
from src.create.prefab_creator import crear_enemy_spawner
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce

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

    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self._toggle_fullscreen()

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.window_size,
                                                  pygame.RESIZABLE)

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

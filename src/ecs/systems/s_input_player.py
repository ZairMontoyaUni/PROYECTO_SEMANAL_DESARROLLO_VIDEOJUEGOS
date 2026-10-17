from typing import Callable
import esper
import pygame
from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(world: esper.World, event: pygame.event.Event,
                        do_action: Callable[[CInputCommand], None]) -> None:
    components = world.get_component(CInputCommand)

    c_input: CInputCommand
    for _entity, c_input in components:
        if event.type == pygame.KEYDOWN and event.key == c_input.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif (event.type == pygame.KEYUP and event.key == c_input.key
              and c_input.phase == CommandPhase.START):
            c_input.phase = CommandPhase.END
            do_action(c_input)
        elif (event.type == pygame.MOUSEBUTTONDOWN
              and event.button == c_input.key):
            c_input.phase = CommandPhase.START
            c_input.pos = pygame.Vector2(event.pos)
            do_action(c_input)

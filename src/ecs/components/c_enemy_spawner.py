import pygame


class SpawnEvent:
    """Un evento de aparición del nivel (ya procesado, sin depender del JSON)."""

    def __init__(self, time: float, enemy_type: str, pos: pygame.Vector2) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.pos = pos
        self.triggered = False


class CEnemySpawner:
    """Guarda la información del nivel cargado y el tiempo transcurrido."""

    def __init__(self, level_data: dict) -> None:
        self.elapsed_time = 0.0
        self.spawn_events: list[SpawnEvent] = []
        for event in level_data.get("enemy_spawn_events", []):
            self.spawn_events.append(
                SpawnEvent(
                    time=event["time"],
                    enemy_type=event["enemy_type"],
                    pos=pygame.Vector2(event["position"]["x"],
                                       event["position"]["y"])
                )
            )
        self.spawn_events.sort(key=lambda e: e.time)

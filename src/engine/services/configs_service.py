import json
from src.engine.services.paths import resource_path


class ConfigsService:
    """Carga archivos de configuración .json una sola vez."""

    def __init__(self) -> None:
        self._configs: dict[str, dict] = {}

    def get(self, path: str) -> dict:
        if path not in self._configs:
            with open(resource_path(path), encoding="utf-8") as cfg_file:
                self._configs[path] = json.load(cfg_file)
        return self._configs[path]

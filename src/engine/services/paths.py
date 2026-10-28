import pathlib
import sys


def resource_path(path: str) -> pathlib.Path:
    """Ruta absoluta de un recurso (relativa a main.py).

    Funciona al ejecutar con Python y también dentro del ejecutable
    creado con PyInstaller.
    """
    base = getattr(sys, "_MEIPASS", None)
    root = pathlib.Path(base) if base else pathlib.Path(__file__).parents[3]
    return root / path

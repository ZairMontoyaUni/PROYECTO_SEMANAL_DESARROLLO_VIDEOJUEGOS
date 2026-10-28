class CSpecialHud:
    """Texto que muestra si el ataque especial está listo o recargando."""

    def __init__(self, ready_info: dict, cooldown_info: dict) -> None:
        self.ready_info = ready_info
        self.cooldown_info = cooldown_info
        self.last_text = ""

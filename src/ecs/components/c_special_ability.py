class CSpecialAbility:
    """Habilidad especial del jugador: tiempo de recarga y tiempo restante."""

    def __init__(self, cooldown: float) -> None:
        self.cooldown = cooldown
        self.time_left = 0.0  # 0 = lista para usarse

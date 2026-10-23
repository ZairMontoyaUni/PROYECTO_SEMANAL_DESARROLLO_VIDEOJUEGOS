class AnimationData:
    """Una animación de la textura: cuadros de inicio y fin, y velocidad."""

    def __init__(self, name: str, start: int, end: int,
                 framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = framerate


class CAnimation:
    """Guarda las animaciones de una entidad y cuál se está reproduciendo."""

    def __init__(self, animations: dict) -> None:
        self.number_frames = animations["number_frames"]
        self.animations: list[AnimationData] = []
        for anim in animations["list"]:
            self.animations.append(AnimationData(anim["name"], anim["start"],
                                                 anim["end"],
                                                 anim["framerate"]))
        self.curr_anim = 0
        self.curr_anim_time = 0.0
        self.curr_frame = self.animations[0].start
        self.finished = False  # True cuando la animación completó una vuelta

    def set_animation(self, name: str) -> None:
        if self.animations[self.curr_anim].name == name:
            return
        for index, anim in enumerate(self.animations):
            if anim.name == name:
                self.curr_anim = index
                self.curr_anim_time = 0.0
                self.curr_frame = anim.start
                self.finished = False
                return

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Horario:
    inicio: datetime

    def __post_init__(self):
        if self.inicio.minute not in (0, 30):
            raise ValueError('O horário deve começar em hora cheia ou meia hora!')
        if self.inicio.second != 0 or self.inicio.microsecond != 0:
            raise ValueError('O horário não pode ter segundos!')
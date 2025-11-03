from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Proceso:
    pid: str
    duracion: int
    prioridad: int
    tiempo_llegada: int = 0
    tiempo_restante: int = field(init=False)
    tiempo_inicio: int | None = field(default=None, init=False)
    tiempo_fin: int | None = field(default=None, init=False)

    def __post_init__(self):
        if not isinstance(self.pid, str) or not self.pid.strip():
            raise ValueError("pid debe ser string no vacío")
        if not isinstance(self.duracion, int) or self.duracion <= 0:
            raise ValueError("duracion debe ser entero positivo")
        if not isinstance(self.prioridad, int):
            raise ValueError("prioridad debe ser entero")
        if not isinstance(self.tiempo_llegada, int) or self.tiempo_llegada < 0:
            raise ValueError("tiempo_llegada debe ser entero ≥ 0")
        self.tiempo_restante = self.duracion

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "duracion": self.duracion,
            "prioridad": self.prioridad,
            "tiempo_llegada": self.tiempo_llegada,
        }

    @staticmethod
    def from_dict(d: dict) -> "Proceso":
        return Proceso(
            pid=d["pid"],
            duracion=int(d["duracion"]),
            prioridad=int(d["prioridad"]),
            tiempo_llegada=int(d.get("tiempo_llegada", 0)),
        )

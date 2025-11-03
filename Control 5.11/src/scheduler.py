from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple
from .proceso import Proceso

GanttEntry = Tuple[str, int, int]  # (pid, t_inicio, t_fin)

class Scheduler(ABC):
    @abstractmethod
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        raise NotImplementedError

class FCFSScheduler(Scheduler):
    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo = 0
        gantt: List[GanttEntry] = []
        for p in procesos:
            inicio = max(tiempo, p.tiempo_llegada)
            if p.tiempo_inicio is None:
                p.tiempo_inicio = inicio
            fin = inicio + p.tiempo_restante
            gantt.append((p.pid, inicio, fin))
            p.tiempo_restante = 0
            p.tiempo_fin = fin
            tiempo = fin
        return gantt

class RoundRobinScheduler(Scheduler):
    def __init__(self, quantum: int = 2):
        if not isinstance(quantum, int) or quantum <= 0:
            raise ValueError("quantum debe ser entero positivo")
        self.quantum = quantum

    def planificar(self, procesos: List[Proceso]) -> List[GanttEntry]:
        tiempo = min((p.tiempo_llegada for p in procesos), default=0)
        cola: List[Proceso] = list(procesos)
        gantt: List[GanttEntry] = []
        while any(p.tiempo_restante > 0 for p in cola):
            for p in cola:
                if p.tiempo_restante <= 0:
                    continue
                if tiempo < p.tiempo_llegada:
                    tiempo = p.tiempo_llegada
                if p.tiempo_inicio is None:
                    p.tiempo_inicio = tiempo
                ejec = min(self.quantum, p.tiempo_restante)
                inicio = tiempo
                fin = inicio + ejec
                gantt.append((p.pid, inicio, fin))
                p.tiempo_restante -= ejec
                tiempo = fin
                if p.tiempo_restante == 0:
                    p.tiempo_fin = fin
        return gantt

from __future__ import annotations
from typing import Dict, List, Optional
from pathlib import Path
import json, csv
from .proceso import Proceso

class RepositorioProcesos:
    def __init__(self):
        self._procesos: Dict[str, Proceso] = {}

    def agregar(self, proceso: Proceso) -> None:
        if proceso.pid in self._procesos:
            raise ValueError(f"Ya existe un proceso con pid {proceso.pid}")
        self._procesos[proceso.pid] = proceso

    def crear_proceso(self, pid: str, duracion: int, prioridad: int, tiempo_llegada: int = 0) -> Proceso:
        nuevo = Proceso(pid, duracion, prioridad, tiempo_llegada=tiempo_llegada)
        self.agregar(nuevo)
        return nuevo

    def eliminar(self, pid: str) -> None:
        if pid not in self._procesos:
            raise KeyError(f"No existe proceso {pid}")
        del self._procesos[pid]

    def obtener(self, pid: str) -> Optional[Proceso]:
        return self._procesos.get(pid)

    def listar(self) -> List[Proceso]:
        return list(self._procesos.values())

    def limpiar(self) -> None:
        self._procesos.clear()

    # Persistencia
    def guardar_json(self, ruta: str | Path) -> None:
        data = [p.to_dict() for p in self.listar()]
        Path(ruta).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def cargar_json(self, ruta: str | Path) -> None:
        data = json.loads(Path(ruta).read_text(encoding="utf-8"))
        self.limpiar()
        for d in data:
            self.agregar(Proceso.from_dict(d))

    def guardar_csv(self, ruta: str | Path) -> None:
        with Path(ruta).open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["pid", "duracion", "prioridad", "tiempo_llegada"])
            for p in self.listar():
                writer.writerow([p.pid, p.duracion, p.prioridad, p.tiempo_llegada])

    def cargar_csv(self, ruta: str | Path) -> None:
        self.limpiar()
        with Path(ruta).open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                self.agregar(Proceso.from_dict(row))

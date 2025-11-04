from __future__ import annotations
from typing import Dict, List
from .proceso import Proceso
from .scheduler import GanttEntry

def calcular_metricas(procesos: List[Proceso], gantt: List[GanttEntry]) -> Dict[str, float]:
    n = len(procesos)
    if n == 0:
        return {"respuesta_media": 0.0, "retorno_media": 0.0, "espera_media": 0.0}
    resp_sum = ret_sum = esp_sum = 0
    for p in procesos:
        if p.tiempo_inicio is None or p.tiempo_fin is None:
            raise ValueError(f"Métricas: proceso {p.pid} no planificado completamente")
        respuesta = p.tiempo_inicio - p.tiempo_llegada
        retorno = p.tiempo_fin - p.tiempo_llegada
        espera = retorno - p.duracion
        resp_sum += respuesta
        ret_sum += retorno
        esp_sum += espera
    return {
        "respuesta_media": resp_sum / n,
        "retorno_media": ret_sum / n,
        "espera_media": esp_sum / n,
    }

# Se verá modificado en base a las metricas y los atributos que correspondan en el enuciado.

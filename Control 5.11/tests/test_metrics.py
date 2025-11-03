from src.proceso import Proceso
from src.metrics import calcular_metricas
from src.scheduler import FCFSScheduler

def test_metricas_fcfs():
    p1 = Proceso("A", 3, 1)
    p2 = Proceso("B", 2, 1)
    procs = [p1, p2]
    gantt = FCFSScheduler().planificar(procs)
    m = calcular_metricas(procs, gantt)
    assert m["respuesta_media"] == (0 + 3) / 2
    assert m["retorno_media"]   == (3 + 5) / 2
    assert m["espera_media"]    == (0 + 3) / 2

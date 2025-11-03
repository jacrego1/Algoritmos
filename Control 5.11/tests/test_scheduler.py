from src.proceso import Proceso
from src.scheduler import FCFSScheduler, RoundRobinScheduler

def reset(procesos):
    for p in procesos:
        p.tiempo_restante = p.duracion
        p.tiempo_inicio = None
        p.tiempo_fin = None

def test_fcfs_gantt_basico():
    p1 = Proceso("P1", 3, 1)
    p2 = Proceso("P2", 2, 1)
    procs = [p1, p2]
    g = FCFSScheduler().planificar(procs)
    assert g == [("P1", 0, 3), ("P2", 3, 5)]
    assert (p1.tiempo_inicio, p1.tiempo_fin) == (0, 3)
    assert (p2.tiempo_inicio, p2.tiempo_fin) == (3, 5)

def test_rr_quantum_2():
    p1 = Proceso("P1", 3, 1)
    p2 = Proceso("P2", 4, 1)
    procs = [p1, p2]
    g = RoundRobinScheduler(quantum=2).planificar(procs)
    assert g[0] == ("P1", 0, 2)
    assert g[1] == ("P2", 2, 4)
    assert p1.tiempo_fin == 5
    assert p2.tiempo_fin == 7

def test_llegadas_no_simultaneas_fcfs():
    p1 = Proceso("A", 3, 1, tiempo_llegada=1)
    p2 = Proceso("B", 2, 1, tiempo_llegada=1)
    g = FCFSScheduler().planificar([p1, p2])
    assert g[0] == ("A", 1, 4)
    assert g[1] == ("B", 4, 6)

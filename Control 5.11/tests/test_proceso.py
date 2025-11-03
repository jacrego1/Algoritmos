from src.proceso import Proceso
import pytest

def test_proceso_valido():
    p = Proceso("A", 5, 1)
    assert p.pid == "A"
    assert p.duracion == 5
    assert p.prioridad == 1
    assert p.tiempo_restante == 5
    assert p.tiempo_llegada == 0

@pytest.mark.parametrize("pid,dur,prio", [("", 5, 1), ("A", 0, 1)])
def test_proceso_invalido(pid, dur, prio):
    with pytest.raises(ValueError):
        Proceso(pid, dur, prio)

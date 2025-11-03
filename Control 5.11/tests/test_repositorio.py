from src.proceso import Proceso
from src.repositorio import RepositorioProcesos
import os, tempfile, pytest

def test_agregar_unicidad():
    r = RepositorioProcesos()
    r.agregar(Proceso("X", 2, 1))
    with pytest.raises(ValueError):
        r.agregar(Proceso("X", 3, 2))

def test_eliminar_y_obtener():
    r = RepositorioProcesos()
    p = r.crear_proceso("ZZ", 1, 1)
    assert r.obtener("ZZ") is p
    r.eliminar("ZZ")
    assert r.obtener("ZZ") is None
    with pytest.raises(KeyError):
        r.eliminar("ZZ")

def test_persistencia_json_y_csv():
    r = RepositorioProcesos()
    r.crear_proceso("P1", 4, 1)
    r.crear_proceso("P2", 2, 2)

    with tempfile.TemporaryDirectory() as d:
        jp = os.path.join(d, "procs.json")
        cp = os.path.join(d, "procs.csv")

        r.guardar_json(jp)
        r2 = RepositorioProcesos()
        r2.cargar_json(jp)
        assert sorted([p.pid for p in r2.listar()]) == ["P1", "P2"]

        r.guardar_csv(cp)
        r3 = RepositorioProcesos()
        r3.cargar_csv(cp)
        assert sorted([p.pid for p in r3.listar()]) == ["P1", "P2"]

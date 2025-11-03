from __future__ import annotations
from .repositorio import RepositorioProcesos
from .scheduler import FCFSScheduler, RoundRobinScheduler
from .metrics import calcular_metricas

def leer_int(msg: str, minimo: int | None = None) -> int:
    while True:
        try:
            v = int(input(msg).strip())
            if minimo is not None and v < minimo:
                print(f"Debe ser un entero >= {minimo}")
                continue
            return v
        except ValueError:
            print("Introduce un entero válido.")

def reset(procs):
    for p in procs:
        p.tiempo_restante = p.duracion
        p.tiempo_inicio = None
        p.tiempo_fin = None

def main():
    repo = RepositorioProcesos()
    # Datos de ejemplo
    repo.crear_proceso("P1", 5, prioridad=2)
    repo.crear_proceso("P2", 3, prioridad=1)
    repo.crear_proceso("P3", 7, prioridad=3)

    while True:
        print("\n=== PLANIFICADOR ===")
        print("1) Añadir proceso")
        print("2) Listar procesos")
        print("3) Eliminar proceso")
        print("4) Planificar (fcfs/rr)")
        print("5) Guardar JSON/CSV")
        print("6) Cargar JSON/CSV")
        print("7) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            pid = input("PID: ").strip()
            dur = leer_int("Duración (>0): ", 1)
            prio = leer_int("Prioridad (int): ")
            tlleg = leer_int("Llegada (>=0): ", 0)
            try:
                repo.crear_proceso(pid, dur, prio, tlleg)
                print("✔ Proceso creado.")
            except ValueError as e:
                print("✖", e)
        elif op == "2":
            for p in repo.listar():
                print(f"{p.pid}: dur={p.duracion}, prio={p.prioridad}, lleg={p.tiempo_llegada}")
        elif op == "3":
            pid = input("PID a eliminar: ").strip()
            try:
                repo.eliminar(pid)
                print("✔ Eliminado.")
            except KeyError as e:
                print("✖", e)
        elif op == "4":
            procs = repo.listar()
            if not procs:
                print("No hay procesos.")
                continue
            reset(procs)
            alg = input("Algoritmo [fcfs/rr]: ").strip().lower()
            if alg == "rr":
                q = leer_int("Quantum (>0): ", 1)
                from .scheduler import RoundRobinScheduler
                sched = RoundRobinScheduler(q)
            else:
                sched = FCFSScheduler()
            gantt = sched.planificar(procs)
            print("\nGantt:")
            for tramo in gantt:
                print(tramo)
            print("Métricas:", calcular_metricas(procs, gantt))
        elif op == "5":
            tipo = input("Formato [json/csv]: ").strip().lower()
            ruta = input("Archivo destino: ").strip()
            if tipo == "json":
                repo.guardar_json(ruta)
            elif tipo == "csv":
                repo.guardar_csv(ruta)
            else:
                print("Formato no válido.")
        elif op == "6":
            tipo = input("Formato [json/csv]: ").strip().lower()
            ruta = input("Archivo origen: ").strip()
            if tipo == "json":
                repo.cargar_json(ruta)
            elif tipo == "csv":
                repo.cargar_csv(ruta)
            else:
                print("Formato no válido.")
        elif op == "7":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()

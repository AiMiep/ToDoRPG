from task_manager_gui import start_task_manager

# Sicherstellen, dass NiceGUI mit Multiprocessing kompatibel ist
if __name__ in {"__main__", "__mp_main__"}:
    start_task_manager()

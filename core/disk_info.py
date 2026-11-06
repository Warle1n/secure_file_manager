import psutil

def show_disks() -> None:
    print("\n--- Диски ---")
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue
        print(f"Устройство: {part.device}")
        print(f"  Точка монтирования: {part.mountpoint}")
        print(f"  ФС: {part.fstype}")
        print(f"  Всего:     {usage.total / (1024**3):.2f} ГБ")
        print(f"  Занято:    {usage.used / (1024**3):.2f} ГБ")
        print(f"  Свободно:  {usage.free / (1024**3):.2f} ГБ")
        print()
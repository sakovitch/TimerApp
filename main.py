import tkinter as tk
from warehouse_selector_module import WarehouseSelector
from timer_app import TimerApp
from update_checker import check_for_update

CURRENT_VERSION = "v1.0.0"  # Aktuálna verzia programu

def main():
    root = tk.Tk()
    warehouse_selector = WarehouseSelector(root)
    root.mainloop()

    selected_warehouse = warehouse_selector.selected_warehouse.get()
    if selected_warehouse:
        root = tk.Tk()
        app = TimerApp(root, selected_warehouse)

        # Skontrolujte aktualizáciu pri spustení
        latest_version = check_for_update(CURRENT_VERSION)
        if latest_version:
            app.prompt_update(latest_version)

        root.mainloop()

if __name__ == "__main__":
    main()

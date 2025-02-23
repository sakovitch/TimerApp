import tkinter as tk
from tkinter import ttk, messagebox
import sys

class WarehouseSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("Vybrať sklad")
        self.master.geometry("300x150")
       
        self.warehouses = ["Poverax EU", "Essex UK"]
        self.selected_warehouse = tk.StringVar()
        self.selection_confirmed = False
       
        label = tk.Label(self.master, text="Vyberte sklad:", font=('Helvetica', 12))
        label.pack(pady=10)
       
        self.combo = ttk.Combobox(self.master, textvariable=self.selected_warehouse,
                                  values=self.warehouses, font=('Helvetica', 12), state='readonly')
        self.combo.pack(pady=10)
       
        button = tk.Button(self.master, text="Potvrdiť", font=('Helvetica', 12), command=self.confirm)
        button.pack(pady=10)
       
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
       
    def confirm(self):
        if self.selected_warehouse.get():
            self.selection_confirmed = True
            self.master.destroy()
        else:
            messagebox.showwarning("Upozornenie", "Prosím, vyberte sklad.")
       
    def on_closing(self):
        if not self.selection_confirmed:
            self.master.destroy()
            sys.exit()
        else:
            self.master.destroy()
       
if __name__ == '__main__':
    root = tk.Tk()
    app = WarehouseSelector(root)
    root.mainloop()
    print("Vybraný sklad:", app.selected_warehouse.get())

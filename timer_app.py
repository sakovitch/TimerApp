import tkinter as tk
from tkinter import Menu, filedialog, ttk, messagebox
from PIL import Image, ImageTk
import time
import os
import pandas as pd
from datetime import datetime
import mysql.connector
from database import get_database_connection
import requests
import zipfile

class TimerApp:
    def prompt_update(self, latest_version):
        """Displays an update prompt."""
        if messagebox.askyesno("Update Available", f"A new version ({latest_version}) is available. Do you want to download it?"):
            self.download_update()

    def download_update(self):
        """Downloads and extracts the new version."""
        url = "https://github.com/sakovitch/TimerApp/archive/refs/heads/main.zip"
        try:
            response = requests.get(url)
            with open("update.zip", "wb") as file:
                file.write(response.content)
            with zipfile.ZipFile("update.zip", "r") as zip_ref:
                zip_ref.extractall("update")
            os.remove("update.zip")
            messagebox.showinfo("Update", "The update has been downloaded successfully.")
            self.update_console("New version downloaded. Restart the application to apply updates.", color="white")
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to download the update: {e}")
            self.update_console(f"Error downloading update: {e}", color="red")

    def update_connection_status(self):
        """Displays database connection status and program version."""
        try:
            conn = get_database_connection()
            conn.close()
            self.status_label.config(text="Connected to DB ✔", fg="green")
            self.update_console("Program is up-to-date.", color="green")
        except Exception as e:
            self.status_label.config(text="Not connected to DB ❗", fg="red")
            self.update_console("Program is outdated or not connected to DB.", color="red")

    def update_console(self, message, color="white"):
        """Adds a message to the console with an optional color."""
        self.console.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n", ("color",))
        self.console.tag_configure("color", foreground=color)
        self.console.see(tk.END)

    def __init__(self, root, warehouse):
        self.root = root
        self.root.title(f"Timer App - {warehouse}")
        self.warehouse = warehouse

        # Color scheme
        self.colors = {
            'bg': '#121212',
            'fg': '#FFFFFF',
            'entry_bg': '#1E1E1E',
            'button_bg': '#2C2C2C',
            'active_bg': '#3C3C3C',
            'font': 'Helvetica'
        }

        main_frame = tk.Frame(root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Console frame on the left
        self.console_frame = tk.Frame(main_frame, bg=self.colors['entry_bg'])
        self.console_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Create the console text widget first
        self.console = tk.Text(self.console_frame, wrap=tk.WORD, bg=self.colors['entry_bg'],
                                fg=self.colors['fg'], font=(self.colors['font'], 10))
        self.console.pack(fill=tk.BOTH, expand=True)

        # Create the status label (appears above the console)
        self.status_label = tk.Label(self.console_frame, text="", font=(self.colors['font'], 10),
                                     bg=self.colors['entry_bg'], fg=self.colors['fg'])
        self.status_label.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Now update connection status after console has been created
        self.update_connection_status()

        # Client buttons at the bottom of the console frame
        self.client_buttons_frame = tk.Frame(self.console_frame, bg=self.colors['entry_bg'])
        self.client_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.clients = ["Mustard", "Musango", "Mousssee", "Trepadora", "Sarah"]
        for client in self.clients:
            btn = tk.Button(self.client_buttons_frame, text=client, font=(self.colors['font'], 10),
                            bg=self.colors['button_bg'], fg=self.colors['fg'],
                            activebackground=self.colors['active_bg'],
                            command=lambda c=client: self.show_client_records(c, clear_console=True))
            btn.pack(side=tk.LEFT, padx=2)

        all_messages_button = tk.Button(self.client_buttons_frame, text="All Messages", font=(self.colors['font'], 10),
                                        bg=self.colors['button_bg'], fg=self.colors['fg'],
                                        activebackground=self.colors['active_bg'],
                                        command=self.show_all_messages)
        all_messages_button.pack(side=tk.LEFT, padx=2)

        # Right panel: logo, version, warehouse info, and timer controls
        right_panel = tk.Frame(main_frame, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.webp")
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.root.iconphoto(False, logo_photo)

        # Logo widget
        self.logo_label = tk.Label(right_panel, image=logo_photo, bg=self.colors['bg'])
        self.logo_label.image = logo_photo
        self.logo_label.pack(pady=10)

        # Version label under the logo
        self.version = "1.0.0"
        self.version_label = tk.Label(right_panel, text=f"Version: {self.version}",
                                      font=(self.colors['font'], 10),
                                      bg=self.colors['bg'], fg=self.colors['fg'])
        self.version_label.pack(pady=5)

        self.warehouse_label = tk.Label(right_panel, text=f"Warehouse: {warehouse}",
                                        font=(self.colors['font'], 14, "bold"),
                                        bg=self.colors['bg'], fg=self.colors['fg'])
        self.warehouse_label.pack(pady=5)

        self.selected_client = tk.StringVar(value=self.clients[0])
        self.client_label = tk.Label(right_panel, text="Select Client:", font=(self.colors['font'], 12),
                                     bg=self.colors['bg'], fg=self.colors['fg'])
        self.client_label.pack(pady=5)
        self.client_menu = ttk.Combobox(right_panel, textvariable=self.selected_client,
                                        values=self.clients, font=(self.colors['font'], 12), state='readonly')
        self.client_menu.pack(pady=5)
        self.client_menu.current(0)

        self.time_label = tk.Label(right_panel, text="0:00:000", font=(self.colors['font'], 48),
                                   bg=self.colors['bg'], fg=self.colors['fg'])
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(right_panel, text="Start/Reset Timer", font=(self.colors['font'], 12),
                                      bg=self.colors['button_bg'], fg=self.colors['fg'],
                                      activebackground=self.colors['active_bg'],
                                      command=self.toggle_timer)
        self.start_button.pack(pady=10)

        self.activity_var = tk.StringVar(value="Packing")
        self.activity_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        self.activity_frame.pack(pady=10)

        self.radio_buttons = []
        for activity in ["Packing", "Work", "Other"]:
            rb = tk.Radiobutton(self.activity_frame, text=activity,
                                variable=self.activity_var, value=activity,
                                font=(self.colors['font'], 12), bg=self.colors['bg'], fg=self.colors['fg'],
                                activebackground=self.colors['active_bg'],
                                selectcolor=self.colors['button_bg'])
            rb.pack(side=tk.LEFT, padx=5)
            self.radio_buttons.append(rb)

        self.custom_activity_entry = tk.Entry(self.activity_frame, font=(self.colors['font'], 12),
                                              state='disabled', bg=self.colors['entry_bg'], fg=self.colors['fg'])
        self.custom_activity_entry.pack(side=tk.LEFT, padx=5)

        self.activity_var.trace('w', self.on_activity_change)

        self.record_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        self.record_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.records_label = tk.Label(self.record_frame, text="Records:", font=(self.colors['font'], 12),
                                      bg=self.colors['bg'], fg=self.colors['fg'])
        self.records_label.pack(anchor='w')

        self.records_listbox = tk.Listbox(self.record_frame, width=70, font=(self.colors['font'], 10),
                                          bg=self.colors['entry_bg'], fg=self.colors['fg'],
                                          selectbackground=self.colors['active_bg'])
        self.records_listbox.pack(fill=tk.BOTH, expand=True)

        self.context_menu = Menu(self.root, tearoff=0, font=(self.colors['font'], 10))
        self.context_menu.add_command(label="Delete Record", command=self.delete_record)
        self.records_listbox.bind("<Button-3>", self.show_context_menu)

        self.buttons_frame = tk.Frame(self.record_frame, bg=self.colors['bg'])
        self.buttons_frame.pack(side=tk.BOTTOM, pady=10)

        self.export_button = tk.Button(self.buttons_frame, text="Export", font=(self.colors['font'], 10),
                                       bg=self.colors['button_bg'], fg=self.colors['fg'],
                                       activebackground=self.colors['active_bg'],
                                       command=self.export_to_excel)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.buttons_frame, text="Save to Database", font=(self.colors['font'], 10),
                                     bg=self.colors['button_bg'], fg=self.colors['fg'],
                                     activebackground=self.colors['active_bg'],
                                     command=self.save_to_database)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0
        self.update_console("Application started", color="white")

    def on_activity_change(self, *args):
        if self.activity_var.get() == "Other":
            self.custom_activity_entry.config(state='normal')
            self.update_console("Activity changed to 'Other'", color="white")
        else:
            self.custom_activity_entry.config(state='disabled')
            self.custom_activity_entry.delete(0, tk.END)
            self.update_console(f"Activity changed to '{self.activity_var.get()}'", color="white")

    def toggle_timer(self):
        if self.is_running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.is_running = True
        self.start_button.config(text="Stop Timer")
        self.start_time = time.time()
        self.update_timer()
        self.update_console("Timer started", color="white")

    def stop_timer(self):
        self.is_running = False
        self.start_button.config(text="Start/Reset Timer")
        formatted_time = self.format_time(int(self.elapsed_time * 1000))
        activity = self.activity_var.get()
        if activity == "Other":
            activity = self.custom_activity_entry.get() or "Other"
        client = self.selected_client.get()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.records_listbox.insert(tk.END, f"{current_datetime} - {client} - {activity}: {formatted_time}")
        self.update_console(f"Timer stopped: {client} - {activity}: {formatted_time}", color="white")

    def update_timer(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            formatted_time = self.format_time(int(self.elapsed_time * 1000))
            self.time_label.config(text=formatted_time)
            self.root.after(10, self.update_timer)

    def format_time(self, milliseconds):
        total_seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}:{seconds:02}:{milliseconds:03}"

    def show_context_menu(self, event):
        try:
            self.records_listbox.selection_clear(0, tk.END)
            self.records_listbox.selection_set(self.records_listbox.nearest(event.y))
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_record(self):
        selected_indices = self.records_listbox.curselection()
        if selected_indices:
            self.records_listbox.delete(selected_indices[0])
            self.update_console("Record deleted", color="white")

    def export_to_excel(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        default_filename = f"EXPORT {current_date}.xlsx"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel File",
            initialfile=default_filename
        )
        if not file_path:
            return

        data = []
        for item in self.records_listbox.get(0, tk.END):
            try:
                datetime_str, rest = item.split(' - ', 1)
                client, rest = rest.split(' - ', 1)
                activity, duration = rest.split(': ', 1)
                data.append([datetime_str, client, activity, duration])
            except ValueError:
                self.update_console(f"Invalid record format: {item}", color="white")
                continue

        df = pd.DataFrame(data, columns=['Date and Time', 'Client', 'Activity', 'Duration'])
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Records', index=False, startrow=1)
        workbook = writer.book
        worksheet = writer.sheets['Records']
        header_format = workbook.add_format({'bold': True, 'font_size': 14})
        worksheet.write('A1', f'Warehouse - {self.warehouse}', header_format)
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        writer.close()
        self.update_console(f"Data exported to '{file_path}'", color="white")

    def save_to_database(self):
        data = []
        for item in self.records_listbox.get(0, tk.END):
            try:
                datetime_str, rest = item.split(' - ', 1)
                client, rest = rest.split(' - ', 1)
                activity, time_val = rest.split(': ', 1)
                data.append([datetime_str, client, activity, time_val])
            except ValueError:
                self.update_console(f"Invalid record format: {item}", color="white")
                continue

        if not data:
            self.update_console("No data to save", color="white")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            for row in data:
                query = """
                INSERT INTO records (datetime, client, activity, duration, warehouse)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (row[0], row[1], row[2], row[3], self.warehouse))
            connection.commit()
            self.update_console("Data successfully saved to database", color="white")
            self.update_connection_status()
        except mysql.connector.Error as error:
            self.update_console(f"Error saving data: {error}", color="red")
            self.status_label.config(text="Not connected to DB ❗", fg="red")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def show_client_records(self, client, clear_console=True):
        if clear_console:
            self.console.delete(1.0, tk.END)
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            query = """
            SELECT datetime, activity, duration FROM records
            WHERE client = %s AND warehouse = %s
            ORDER BY datetime DESC
            """
            cursor.execute(query, (client, self.warehouse))
            records = cursor.fetchall()
            self.update_console(f"Records for client {client} in warehouse {self.warehouse}:", color="white")
            if records:
                for record in records:
                    self.update_console(f"{record[0]} - {record[1]}: {record[2]}", color="white")
            else:
                self.update_console("No records found.", color="white")
        except mysql.connector.Error as error:
            self.update_console(f"Error loading records: {error}", color="red")
            self.status_label.config(text="Not connected to DB ❗", fg="red")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def show_all_messages(self):
        self.console.delete(1.0, tk.END)
        self.update_console("Displaying all messages:", color="white")
        for client in self.clients:
            self.show_client_records(client, clear_console=False)

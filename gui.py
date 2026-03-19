import tkinter as tk
from tkinter import ttk, messagebox

import db_manager


class RoomMangerApp:
    def __init__(self, root_window):
        self.window = root_window
        self.window.title("Room Booking Dashboard")
        self.window.geometry("550x500")
        self.window.configure(padx=20, pady=20, bg='#f4f6f9')
        self.window.configure(padx=20, pady=20)
        self.build_screen()
        self.load_rooms_from_database()

    def build_screen(self):
        """Builds all the text boxes, buttons and lists on the screen"""

        # Title
        title_label = ttk.Label(
            self.window,
            text="Room Manager System",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 15))

        # Input section
        input_frame = ttk.Frame(self.window)
        input_frame.pack(fill="x", pady=10)

        # Room Name Input
        ttk.Label(
            input_frame,
            text="Room Name (e.g, Room A):"
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.room_name_box = ttk.Entry(input_frame, width=30)
        self.room_name_box.grid(row=0, column=1, padx=10, pady=5)

        # Capacity Input
        ttk.Label(
            input_frame,
            text="Capacity (number only):"
        ).grid(row=1, column=0, sticky="w", pady=5)
        self.capacity_box = ttk.Entry(input_frame, width=30)
        self.capacity_box.grid(row=1, column=1, padx=10, pady=5)

        # Buttons section
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=15)

        # action function
        ttk.Button(
            button_frame,
            text="Add New Room",
            command=self.action_add_room
        ).grid(row=0, column=0, padx=5)
        ttk.Button(
            button_frame,
            text="Update Capacity",
            command=self.action_update_room
        ).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame,
                   text="Remove Room",
                   command=self.action_remove_room
                   ).grid(row=0, column=2, padx=5)

        # display section
        ttk.Label(
            self.window,
                  text="Currently Available Rooms:",
                  font=("Arial", 10, "bold")
        ). pack(anchor="w")

        # Listbox to show the rooms
        self.room_display_list = tk.Listbox(
            self.window,
            height=12,
            font=("Courier", 10))
        self.room_display_list.pack(fill="both", expand=True, pady=5)

    def load_rooms_from_database(self):
        """Ask the db_manager for the rooms and display them in the list"""
        self.room_display_list.delete(0, tk.END)  # clear the old list

        rooms = db_manager.get_all_rooms()
        for room in rooms:
            room_id = room[0]
            name = room[1]
            capacity = room[2]

            display_text = (f"ID: {room_id: <4} | "
                            f"Name: {name: <15} |"
                            f" Capacity: {capacity}")
            self.room_display_list.insert(tk.END, display_text)

    def action_add_room(self):
        name = self.room_name_box.get().strip()
        capacity_text = self.capacity_box.get().strip()

        if not name or not capacity_text.isdigit():
            messagebox.showwarning(
                "Error",
                "Please type a valid room name and a number for capacity"
            )
            return

        success, message = db_manager.add_room(name, int(capacity_text))
        if success:
            messagebox.showinfo("Success", message)
            self.room_name_box.delete(0, tk.END)
            self.capacity_box.delete(0, tk.END)
            self.load_rooms_from_database()  # refresh the screen
        else:
            messagebox.showerror("Database Error", message)

    def action_update_room(self):
        name = self.room_name_box.get().strip()
        capacity_text = self.capacity_box.get().strip()

        if not name or not capacity_text.isdigit():
            messagebox.showwarning(
                "Error",
                "Please type a valid room name and a number for update"
            )
            return

        success, message = db_manager.update_room(name, int(capacity_text))
        if success:
            messagebox.showinfo("Success", message)
            self.capacity_box.delete(0, tk.END)
            self.load_rooms_from_database()  # refresh the screen
        else:
            messagebox.showerror("Database Error", message)

    def action_remove_room(self):
        name = self.room_name_box.get().strip()

        if not name:
            messagebox.showwarning(
                "Error",
                "Please type a valid  name to delete"
            )
            return

        confirm = messagebox.askyesno(
            "confirm Deletion",
            f"Are you sure you want to permanently delete'{name}' " 
                    f"and cancel all its reservations?"
        )
        if confirm:
            success, message = db_manager.remove_room(name)
            if success:
                messagebox.showinfo("Room Removed", message)
                self.room_name_box.delete(0, tk.END)
                self.load_rooms_from_database()
            else:
                messagebox.showerror("Database Error", message)


if __name__ == "__main__":
    main_window = tk.Tk()
    app = RoomMangerApp(main_window)
    main_window.mainloop()

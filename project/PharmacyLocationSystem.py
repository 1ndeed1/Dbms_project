import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector

class PharmacyLocationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Fisa Pharmacy - Location Management")
        self.root.geometry("800x800")
        self.root.configure(bg="#f3f4f6")

        # Initialize database
        self.init_database()

        # Create main container
        self.main_container = tk.Frame(
            root,
            bg="white",
            bd=1,
            relief="solid"
        )
        self.main_container.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Create and pack components
        self.create_logo_section()
        self.create_title()
        self.create_form()
        self.create_search_section()
        self.create_table()
        
        # Create alert container
        self.alert_label = tk.Label(
            self.main_container,
            text="",
            bg="white",
            fg="green",
            font=("Arial", 10)
        )
        self.alert_label.pack(pady=10)

        # Load existing locations
        self.load_existing_locations()

    def init_database(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="AbHi2551968",
            database="pharmacy"
        )
        self.cursor = self.db.cursor()
        
        # Create medicines table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2),
                quantity INT
            )
        ''')
        
        # Create medicine_locations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_locations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                medicine_id INT,
                location_type VARCHAR(255) NOT NULL,
                location_number VARCHAR(255) NOT NULL,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medicine_id) REFERENCES medicines(id) ON DELETE CASCADE
            )
        ''')
        self.db.commit()

    def create_logo_section(self):
        # ... (unchanged)
        pass

    def create_title(self):
        # ... (unchanged)
        pass

    def create_form(self):
        # ... (unchanged)
        pass

    def create_search_section(self):
        # ... (unchanged)
        pass

    def create_table(self):
        # ... (unchanged)
        pass

    def load_existing_locations(self):
        self.cursor.execute("""
            SELECT m.name, ml.location_type, ml.location_number 
            FROM medicine_locations ml
            JOIN medicines m ON ml.medicine_id = m.id
        """)
        rows = self.cursor.fetchall()
        
        for row in rows:
            self.tree.insert("", "end", values=(row[0], f"{row[1]} {row[2]}"))

    def add_location(self):
        medicine = self.medicine_entry.get().strip()
        location_type = self.location_type.get()
        location_number = self.location_entry.get().strip()
        
        if medicine and location_number:
            # Check if medicine exists
            self.cursor.execute("SELECT id FROM medicines WHERE name = %s", (medicine,))
            result = self.cursor.fetchone()
            
            if result:
                medicine_id = result[0]
                self.cursor.execute("INSERT INTO medicine_locations (medicine_id, location_type, location_number) VALUES (%s, %s, %s)", (medicine_id, location_type, location_number))
                self.db.commit()
                self.tree.insert("", "end", values=(medicine, f"{location_type} {location_number}"))
                self.show_alert("Location added successfully!")
                self.medicine_entry.delete(0, tk.END)
                self.location_entry.delete(0, tk.END)
            else:
                self.show_alert("Medicine not found in the database!", "error")
        else:
            self.show_alert("Please fill all fields!", "error")

    def search_medicine(self):
        medicine = self.search_entry.get().strip()
        self.tree.delete(*self.tree.get_children())
        
        if medicine:
            self.cursor.execute("""
                SELECT m.name, ml.location_type, ml.location_number 
                FROM medicine_locations ml
                JOIN medicines m ON ml.medicine_id = m.id
                WHERE m.name LIKE %s
            """, (f"%{medicine}%",))
            rows = self.cursor.fetchall()
            
            for row in rows:
                self.tree.insert("", "end", values=(row[0], f"{row[1]} {row[2]}"))
        else:
            self.load_existing_locations()

    def show_alert(self, message, type_="success"):
        self.alert_label.config(text=message)
        if type_ == "success":
            self.alert_label.config(fg="green")
        else:
            self.alert_label.config(fg="red")
        self.root.after(3000, lambda: self.alert_label.config(text=""))

def main():
    root = tk.Tk()
    app = PharmacyLocationSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
import subprocess  # Add this import at the top of the file

class MedicinePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Page - Fisa Pharmacy")
        
        # Set window size and center it
        window_width = 800
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg='#F4F4EE')

        # Connect to the database
        self.conn = self.create_connection()
        self.create_db_table()

        # Create background shapes
        self.create_background_shapes()
        
        # Create main container
        self.create_main_container()

    def create_connection(self):
        """ Create a database connection to the MySQL database """
        try:
            conn = mysql.connector.connect(
                host='localhost',  # Change if needed
                database='pharmacy',
                user='root',  # Replace with your MySQL username
                password='AbHi2551968'  # Replace with your MySQL password
            )
            if conn.is_connected():
                print("Connected to MySQL database")
                return conn
        except Error as e:
            print(f"Error: {e}")
            return None

    def create_db_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS medicines (
                            sku VARCHAR(255) PRIMARY KEY,
                            name VARCHAR(255),
                            manufacturer VARCHAR(255),
                            dosage_form VARCHAR(255),
                            strength VARCHAR(255),
                            expiration_date DATE)''')
        self.conn.commit()

    def create_background_shapes(self):
        self.bg_canvas = tk.Canvas(
            self.root,
            width=800,
            height=800,
            bg='#F4F4EE',
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)
        self.bg_canvas.create_oval(-100, 50, 150, 300, fill='#FF6F3C', stipple='gray50')
        self.bg_canvas.create_oval(650, 600, 800, 750, fill='#FF6F3C', stipple='gray50')
        self.bg_canvas.create_rectangle(120, 150, 220, 250, fill='#333333', stipple='gray50')
        self.bg_canvas.create_rectangle(580, 500, 680, 600, fill='#333333', stipple='gray50')

    def create_main_container(self):
        self.container = tk.Frame(
            self.root,
            bg='white',
            bd=1,
            relief='solid'
        )
        self.container.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        self.create_logo_section()
        self.create_title()
        self.create_form()
        self.create_table()
        self.create_home_button()  # Add this line to create the home button

    def create_logo_section(self):
        logo_frame = tk.Frame(self.container, bg='white')
        logo_frame.pack(pady=20)
        
        try:
            logo_img = Image.open("logo.jpg")
            logo_img = logo_img.resize((80, 80), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo_photo, bg='white').pack()
        except:
            tk.Label(logo_frame , text="Logo", bg='white').pack()

    def create_title(self):
        title_frame = tk.Frame(self.container, bg='white')
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Medicine Page", font=("Arial", 24), bg='white').pack()

    def create_form(self):
        form_frame = tk.Frame(self.container, bg='white')
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Enter Medicine Details:", font=("Arial", 16), bg='white').pack(pady=10)
        
        self.sku_entry = tk.Entry(form_frame, width=30)
        self.sku_entry.pack(pady=5)
        
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.pack(pady=5)
        
        self.manufacturer_entry = tk.Entry(form_frame, width=30)
        self.manufacturer_entry.pack(pady=5)
        
        self.dosage_form_entry = tk.Entry(form_frame, width=30)
        self.dosage_form_entry.pack(pady=5)
        
        self.strength_entry = tk.Entry(form_frame, width=30)
        self.strength_entry.pack(pady=5)
        
        self.expiration_date_entry = tk.Entry(form_frame, width=30)
        self.expiration_date_entry.pack(pady=5)
        
        tk.Button(form_frame, text="Add Medicine", command=self.add_medicine).pack(pady=10)

    def create_table(self):
        table_frame = tk.Frame(self.container, bg='white')
        table_frame.pack(pady=10)
        
        self.tree = ttk.Treeview(table_frame)
        self.tree.pack(pady=10)
        
        self.tree['columns'] = ('sku', 'name', 'manufacturer', 'dosage_form', 'strength', 'expiration_date')
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("sku", anchor=tk.W, width=100)
        self.tree.column("name", anchor=tk.W, width=100)
        self.tree.column("manufacturer", anchor=tk.W, width=100)
        self.tree.column("dosage_form", anchor=tk.W, width=100)
        self.tree.column("strength", anchor=tk.W, width=100)
        self.tree.column("expiration_date", anchor=tk.W, width=100)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("sku", text="SKU", anchor=tk.W)
        self.tree.heading("name", text="Name", anchor=tk.W)
        self.tree.heading("manufacturer", text="Manufacturer", anchor=tk.W)
        self.tree.heading("dosage_form", text="Dosage Form", anchor=tk.W)
        self.tree.heading("strength", text="Strength", anchor=tk.W)
        self.tree.heading("expiration_date", text="Expiration Date", anchor=tk.W)
        
        self.tree.pack()

    def add_medicine(self):
        sku = self.sku_entry.get()
        name = self.name_entry.get()
        manufacturer = self.manufacturer_entry.get()
        dosage_form = self.dosage_form_entry.get()
        strength = self.strength_entry.get()
        expiration_date = self.expiration_date_entry.get()
        
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO medicines (sku, name, manufacturer, dosage_form, strength, expiration_date) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (sku, name, manufacturer, dosage_form, strength , expiration_date))
        self.conn.commit()
        
        self.tree.insert('', 'end', values=(sku, name, manufacturer, dosage_form, strength, expiration_date))

    def create_home_button(self):
        home_button = tk.Button(
            self.container,
            text="Go to Home",
            command=self.go_to_home,
            bg='#FF6F3C',
            fg='white',
            font=("Arial", 12)
        )
        home_button.pack(pady=10)

    def go_to_home(self):
        self.root.destroy()  # Close the current window
        subprocess.run(["python", "home.py"])  # Run the home.py file

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicinePage(root)
    root.mainloop()
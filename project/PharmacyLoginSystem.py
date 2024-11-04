import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import sys

class PharmacySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Fisa Pharmacy - Login")
        
        # Set window size and center it
        window_width = 400
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg='#f0f2f5')

        # Create main container
        self.login_container = tk.Frame(
            root,
            bg='white',
            bd=0,
            relief='solid',
            width=350,
            height=500
        )
        self.login_container.place(relx=0.5, rely=0.5, anchor='center')
        self.login_container.pack_propagate(False)

        # Initialize database
        self.init_database()

        # Create and pack components
        self.create_logo_section()
        self.create_login_form()

    def init_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AbHi2551968",
                database="pharmacy"
            )
            self.cursor = self.conn.cursor()
            
            # Create users table if it doesn't exist
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                (id INT AUTO_INCREMENT PRIMARY KEY,
                                username VARCHAR(255) UNIQUE NOT NULL,
                                password VARCHAR(255) NOT NULL)''')
            self.conn.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def create_logo_section(self):
        # Logo section
        logo_frame = tk.Frame(self.login_container, bg='white')
        logo_frame.pack(fill='x', pady=20)
        
        # Title
        title_label = tk.Label(
            logo_frame,
            text="Fisa Pharmacy",
            font=("Arial", 24, "bold"),
            bg='white'
        )
        title_label.pack(pady=10)

    def create_login_form(self):
        # Login form
        form_frame = tk.Frame(self.login_container, bg='white')
        form_frame.pack(fill='x', padx=40)

        # Username entry
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bd=1,
            relief="solid"
        )
        self.username_entry.insert(0, "Enter your username")
        self.username_entry.bind('<FocusIn>', lambda e: self.on_entry_click(self.username_entry, "Enter your username"))
        self.username_entry.bind('<FocusOut>', lambda e: self.on_focus_out(self.username_entry, "Enter your username"))
        self.username_entry.pack(fill='x', pady=10)

        # Password entry
        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            bd=1,
            relief="solid"
        )
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind('<FocusIn>', lambda e: self.on_entry_click(self.password_entry, "Enter your password"))
        self.password_entry.bind('<FocusOut>', lambda e: self.on_focus_out(self.password_entry, "Enter your password"))
        self.password_entry.pack(fill='x', pady=10)

        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.login,
            cursor="hand2"
        )
        login_btn.pack(fill='x', pady=20)

        # Create account button
        create_account_btn = tk.Button(
            form_frame,
            text="Create New Account",
            bg="#FF6F3C",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.show_create_account,
            cursor="hand2"
        )
        create_account_btn.pack(fill='x')

    def on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            if placeholder == "Enter your password":
                entry.config(show="•")

    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Enter your password":
                entry.config(show="")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "Enter your username" or password == "Enter your password":
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        if self.check_credentials(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.root.withdraw()  # Hide the login window
            try:
                os.system('python home.py')  # Run home.py
                self.root.destroy()  # Close the login window after home.py is closed
            except Exception as e:
                messagebox.showerror("Error", f"Could not open home page: {str(e)}")
                self.root.deiconify()  # Show login window again if there's an error
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def check_credentials(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            result = self.cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return False

    def show_create_account(self):
        for widget in self.login_container.winfo_children():
            widget.destroy()

        form_frame = tk.Frame(self.login_container, bg='white')
        form_frame.pack(fill='x', padx=40, pady=20)

        tk.Label(form_frame, text="Create Account", font=("Arial", 18, "bold"), bg='white').pack(pady=(0, 20))

        tk.Label(form_frame, text="Username", anchor='w', bg='white', font=("Arial", 10)).pack(fill='x', pady=(0, 5))
        self.new_username_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.new_username_entry.pack(fill='x', pady=(0, 15))

        tk.Label(form_frame, text="Password", anchor='w', bg='white', font=("Arial", 10)).pack(fill='x', pady=(0, 5))
        self.new_password_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid", show="•")
        self.new_password_entry.pack(fill='x', pady=(0, 15))

        tk.Label(form_frame, text="Confirm Password", anchor='w', bg='white', font=("Arial", 10)).pack(fill='x', pady=(0, 5))
        self.confirm_password_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid", show="•")
        self.confirm_password_entry.pack(fill='x', pady=(0, 20))

        create_btn = tk.Button(
            form_frame,
            text="Create Account",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.create_account,
            cursor="hand2"
        )
        create_btn.pack(fill='x', pady=(10, 0))

        back_btn = tk.Button(
            form_frame,
            text="Back to Login",
            bg="#FF6F3C",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.show_login,
            cursor="hand2"
        )
        back_btn.pack(fill='x', pady=(10, 0))

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please enter all fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_login(self):
        for widget in self.login_container.winfo_children():
            widget.destroy()

        self.create_logo_section()
        self.create_login_form()

def main():
    root = tk.Tk()
    app = PharmacySystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess

class PharmacyCustomerSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Fisa Pharmacy - Customer Management")
        self.root.geometry("800x800")
        self.root.configure(bg="#f3f4f6")

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="AbHi2551968", 
            database="pharmacy"
        )
        self.cursor = self.conn.cursor()

        # Create main container with white background and rounded corners
        self.main_container = tk.Frame(root, bg="white", bd=1, relief="solid")
        self.main_container.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Create and pack the logo container
        self.create_logo_section()
        
        # Create and pack the title
        self.create_title()
        
        # Create and pack the form
        self.create_form()
        
        # Create and pack the table
        self.create_table()
        
        # Create alert container
        self.alert_label = tk.Label(self.main_container, text="", bg="white", fg="green", font=("Arial", 10))
        self.alert_label.pack(pady=10)

    def create_logo_section(self):
        logo_frame = tk.Frame(self.main_container, bg="white")
        logo_frame.pack(pady=20)
        
        try:
            logo_img = Image.open("logo.jpg").resize((150, 150), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(logo_frame, image=self.logo_photo, bg="white").pack()
        except:
            tk.Label(logo_frame, text="LOGO", bg="white", font=("Arial", 24)).pack()

        pharmacy_name = tk.Label(logo_frame, text="Fisa Pharmacy", font=("Arial", 28, "bold"), fg="#e87e04", bg="white")
        pharmacy_name.pack()

    def create_title(self):
        title = tk.Label(self.main_container, text="Customer Page", font=("Arial", 20), bg="white", fg="#333333")
        title.pack(pady=10)

    def create_form(self):
        form_frame = tk.Frame(self.main_container, bg="white")
        form_frame.pack(fill="x", padx=20)

        # Form Fields
        fields = [("Customer ID", "id_entry"), 
                  ("Customer Name", "name_entry"), 
                  ("Medicine Purchased", "medicine_entry"), 
                  ("Phone Number", "phone_entry")]

        for label, attr in fields:
            tk.Label(form_frame, text=label, bg="white", font=("Arial", 10)).pack(anchor="w")
            setattr(self, attr, tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid"))
            getattr(self, attr).pack(fill="x", pady=(5, 15))

        # Submit Button
        submit_btn = tk.Button(
            form_frame, text="Add Customer", bg="#e87e04", fg="white",
            font=("Arial", 12), command=self.add_customer, relief="flat", padx=20, pady=5
        )
        submit_btn.pack(fill="x", pady=10)

        # Retrieve Button
        retrieve_btn = tk.Button(
            form_frame, text="Retrieve Customers", bg="#333333", fg="white",
            font=("Arial", 12), command=self.retrieve_customers, relief="flat", padx=20, pady=5
        )
        retrieve_btn.pack(fill="x", pady=10)

        # Back to Home Button
        home_btn = tk.Button(
            form_frame, text="Back to Home", bg="#333333", fg="white",
            font=("Arial", 12), command=self.back_to_home, relief="flat", padx=20, pady=5
        )
        home_btn.pack(fill="x", pady=10)

    def create_table(self):
        tk.Label(self.main_container, text="Customer List", font=("Arial", 16), bg="white", fg="#333333").pack(pady=20)

        columns = ("Customer ID", "Customer Name", "Medicine Purchased", "Phone Number")
        self.tree = ttk.Treeview(self.main_container, columns=columns, show="headings", height=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", background="#e87e04", foreground="white", font=("Arial", 10, "bold"))

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")

        self.tree.pack(padx=20, pady=10)

    def add_customer(self):
        customer_id = self.id_entry.get()
        name = self.name_entry.get()
        medicine = self.medicine_entry.get()
        phone = self.phone_entry.get()
        
        if all([customer_id, name, medicine, phone]):
            try:
                # Insert into database
                query = "INSERT INTO customers (customer_id, name, medicine, phone) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, (customer_id, name, medicine, phone))
                self.conn.commit()
                
                # Insert into tree view
                self.tree.insert("", "end", values=(customer_id, name, medicine, phone))
                
                # Show popup message with customer details
                details_message = f"""
Customer Details Added Successfully:
--------------------------------
Customer ID: {customer_id}
Name: {name}
Medicine: {medicine}
Phone: {phone}
--------------------------------"""
                messagebox.showinfo("Success", details_message)
                
                # Clear entries
                for field in [self.id_entry, self.name_entry, self.medicine_entry, self.phone_entry]:
                    field.delete(0, tk.END)
                    
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
                
        else:
            messagebox.showwarning("Warning", "Please fill all fields!")

    def retrieve_customers(self):
        try:
            self.tree.delete(*self.tree.get_children())
            query = "SELECT * FROM customers"
            self.cursor.execute(query)
            customers = self.cursor.fetchall()
            
            if customers:
                for customer in customers:
                    self.tree.insert("", "end", values=customer)
                messagebox.showinfo("Success", f"Retrieved {len(customers)} customer records successfully!")
            else:
                messagebox.showinfo("Info", "No customer records found in the database.")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving customers: {err}")

    def back_to_home(self):
        self.close_db_connection()  # Close the database connection
        self.root.destroy()
        subprocess.Popen(['python', 'home.py'])  # Opens the home page file

    def close_db_connection(self):
        self.cursor.close()
        self.conn.close()

def main():
    root = tk.Tk()
    app = PharmacyCustomerSystem(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close_db_connection(), root.destroy()))  # Close DB on exit
    root.mainloop()

if __name__ == "__main__":
    main()
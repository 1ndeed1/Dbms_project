import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime
from tkcalendar import DateEntry

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Fisa Pharmacy - Billing Page")
        self.root.geometry("800x800")
        self.root.configure(bg="#f3f4f6")

        # Initialize database
        self.setup_database()

        # Main container
        self.main_container = tk.Frame(root, bg="white", bd=1, relief="solid")
        self.main_container.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.create_header()
        self.create_form()
        self.create_table()
        
        # Alert label for messages
        self.alert_label = tk.Label(
            self.main_container,
            text="",
            bg="white",
            fg="green",
            font=("Arial", 10)
        )
        self.alert_label.pack(pady=10)

    def create_header(self):
        header_frame = tk.Frame(self.main_container, bg="white")
        header_frame.pack(pady=20)
        
        pharmacy_name = tk.Label(
            header_frame,
            text="FISA PHARMACY",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#e87e04"
        )
        pharmacy_name.pack()

        title_label = tk.Label(
            header_frame,
            text="Billing System",
            font=("Arial", 18),
            bg="white",
            fg="#333333"
        )
        title_label.pack(pady=10)

    def setup_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AbHi2551968",
                database="pharmacy"
            )
            self.cursor = self.conn.cursor()

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS billing (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    medicine_name VARCHAR(255) NOT NULL,
                    prescription_weeks INT,
                    date_purchased DATE,
                    amount_paid DECIMAL(10,2)
                )
            ''')
            self.conn.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_form(self):
        form_frame = tk.Frame(self.main_container, bg="white")
        form_frame.pack(fill="x", padx=20)

        # Medicine Name Field
        tk.Label(form_frame, text="Medicine Name", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.medicine_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.medicine_entry.pack(fill="x", pady=(5, 15))

        # Prescription Weeks Field
        tk.Label(form_frame, text="Prescription (weeks)", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.weeks_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.weeks_entry.pack(fill="x", pady=(5, 15))

        # Amount Field
        tk.Label(form_frame, text="Amount", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.amount_entry = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.amount_entry.pack(fill="x", pady=(5, 15))

        # Date Purchased Field
        tk.Label(form_frame, text="Date Purchased", bg="white", font=("Arial", 10)).pack(anchor="w")
        self.date_entry = DateEntry(form_frame, width=12, background='darkblue', 
                                  foreground='white', borderwidth=2, 
                                  date_pattern='yyyy-mm-dd')
        self.date_entry.pack(fill="x", pady=(5, 15))

        # Submit Button
        submit_btn = tk.Button(
            form_frame,
            text="Add to Bill",
            bg="#e87e04",
            fg="white",
            font=("Arial", 12),
            command=self.add_to_bill,
            relief="flat",
            padx=20,
            pady=5
        )
        submit_btn.pack(fill="x", pady=10)

    def create_table(self):
        # Table Title
        tk.Label(
            self.main_container,
            text="Billing Items",
            font=("Arial", 16),
            bg="white",
            fg="#333333"
        ).pack(pady=20)

        # Create Table
        columns = ("Medicine Name", "Prescription (weeks)", "Date Purchased", "Amount")
        self.tree = ttk.Treeview(
            self.main_container,
            columns=columns,
            show="headings",
            height=10
        )

        # Style the table
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            background="#e87e04",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(padx=20, pady=10)

    def add_to_bill(self):
        medicine = self.medicine_entry.get()
        weeks = self.weeks_entry.get()
        amount = self.amount_entry.get()
        date_purchased = self.date_entry.get_date().strftime('%Y-%m-%d')

        if medicine and weeks and amount:
            try:
                # Insert into database
                sql = '''
                    INSERT INTO billing (medicine_name, prescription_weeks, date_purchased, amount_paid)
                    VALUES (%s, %s, %s, %s)
                '''
                values = (medicine, int(weeks), date_purchased, float(amount))
                self.cursor.execute(sql, values)
                self.conn.commit()

                # Add to treeview
                self.tree.insert("", "end", values=(medicine, weeks, date_purchased, amount))
                
                # Clear entries
                self.medicine_entry.delete(0, tk.END)
                self.weeks_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.date_entry.set_date(None)
                
                self.show_alert("Item added to bill successfully!")
                
            except mysql.connector.Error as err:
                self.show_alert(f"Database error: {str(err)}", "error")
            except ValueError:
                self.show_alert("Please enter valid numbers for weeks and amount", "error")
        else:
            self.show_alert("Please fill all required fields!", "error")

    def show_alert(self, message, type_="success"):
        self.alert_label.config(text=message)
        if type_ == "success":
            self.alert_label.config(fg="green")
        else:
            self.alert_label.config(fg="red")
        self.root.after(3000, lambda: self.alert_label.config(text=""))

    def __del__(self):
        if hasattr(self, 'conn'):
            self.cursor.close()
            self.conn.close()

def main():
    root = tk.Tk()
    app = BillingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
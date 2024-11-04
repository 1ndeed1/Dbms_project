import tkinter as tk
import subprocess

class ResponsiveUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Medical Management System")
        self.geometry("400x300")
        self.configure(bg="#F4F4EE")
        self.minsize(200, 150)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.bind("<Configure>", self.on_resize)
        
        self.create_widgets()

    def create_widgets(self):
        # Main container
        self.main_container = tk.Frame(self, bg="#F4F4EE")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = tk.Frame(self.main_container, bg="#333333")
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.header_label = tk.Label(self.header_frame, text="Employee Portal", 
                                   bg="#333333", fg="#FFFFFF")
        self.header_label.grid(row=0, column=0, pady=2)

        self.sub_header = tk.Label(self.header_frame, 
                                 text="Access and manage resources",
                                 bg="#333333", fg="#FFFFFF")
        self.sub_header.grid(row=1, column=0, pady=1)

        # Content area
        self.content_frame = tk.Frame(self.main_container, bg="#FFFFFF")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Buttons container
        self.button_frame = tk.Frame(self.content_frame, bg="#FFFFFF")
        self.button_frame.grid(row=1, column=0, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.buttons = [
            ("Logout", "PharmacyLoginSystem.py"),  # New login button
            ("Medicines", "MedicinePage.py"),
            ("Billing", "BillingSystem.py"),
            ("Customers", "Customer.py"),
            ("Inventory", "PharmacyLocationSystem.py"),
            ("Users", "PharmacyLoginSystem.py"),
        ]

        for i, (text, page) in enumerate(self.buttons):
            btn = tk.Button(self.button_frame, text=text, bg="#FF6F3C", fg="#FFFFFF",
                          command=lambda p=page: self.open_page(p))
            btn.grid(row=i, column=0, pady=2, padx=5, sticky="ew")

        self.update_font_sizes()

    def open_page(self, page_name):
        self.destroy()
        subprocess.Popen(['python', page_name])

    def on_resize(self, event):
        if event.widget == self:
            self.update_font_sizes()

    def update_font_sizes(self):
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        header_size = min(int(window_height * 0.04), int(window_width * 0.04))
        subheader_size = max(int(header_size * 0.8), 6)
        button_size = max(int(header_size * 0.9), 6)

        header_size = min(header_size, 20)
        subheader_size = min(subheader_size, 16)
        button_size = min(button_size, 14)

        self.header_label.configure(font=("Arial", header_size, "bold"))
        self.sub_header.configure(font=("Arial", subheader_size))

        for child in self.button_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(font=("Arial", button_size))
                
        padding_x = max(int(window_width * 0.01), 2)
        padding_y = max(int(window_height * 0.01), 1)
        
        for child in self.button_frame.winfo_children():
            child.grid_configure(padx=padding_x, pady=padding_y)

if __name__ == "__main__":
    app = ResponsiveUI()
    app.mainloop()
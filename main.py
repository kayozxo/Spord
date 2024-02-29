import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Password App")
        self.root.geometry("500x500")

        self.password_set = False
        self.key = None
        self.password_file = None
        self.password_dict = {}

        self.check_password()

        self.login_frame = tk.Frame(root)

        self.label_login = tk.Label(self.login_frame, text="Enter Password:", pady=10)
        self.label_login.pack()

        self.password_entry_login = tk.Entry(self.login_frame, show="*")
        self.password_entry_login.pack(pady=10)

        self.submit_button_login = tk.Button(self.login_frame, text="Login", command=self.check_login)
        self.submit_button_login.pack(pady=10)

        self.password_setup_frame = tk.Frame(root)

        self.label_setup = tk.Label(self.password_setup_frame, text="Set Password:", pady=10)
        self.label_setup.pack()

        self.password_entry_setup = tk.Entry(self.password_setup_frame, show="*")
        self.password_entry_setup.pack(pady=10)

        self.submit_button_setup = tk.Button(self.password_setup_frame, text="Submit", command=self.save_password)
        self.submit_button_setup.pack(pady=10)

        self.main_frame = tk.Frame(root)

        self.label_main = tk.Label(self.main_frame, text="Welcome to the App!", font=('Helvetica', 12), pady=20)
        self.label_main.pack()

        self.button_main = tk.Button(self.main_frame, text="Logout", command=self.logout)
        self.button_main.pack(pady=10)

        instructions = '''To add password fill all the fields and press "Add Password"
        To view password, enter Account Name and press "Get Password"'''

        self.instruction_label = tk.Label(self.main_frame,  text=instructions, bg="#d3d3d3")
        self.instruction_label.pack(padx=10, pady=5)

        self.service_label = tk.Label(self.main_frame, text="Account:", bg="#d3d3d3")
        self.service_label.pack(padx=10, pady=5)
        self.service_entry = tk.Entry(self.main_frame)
        self.service_entry.pack(padx=10, pady=5)

        self.username_label = tk.Label(self.main_frame, text="Username:", bg="#d3d3d3")
        self.username_label.pack(padx=10, pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(padx=10, pady=5)

        self.password_label = tk.Label(self.main_frame, text="Password:", bg="#d3d3d3")
        self.password_label.pack(padx=10, pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(padx=10, pady=5)


        self.add_button = tk.Button(self.main_frame, text="Add Password", command=self.add_password, height=1, width=10)
        self.add_button.pack(padx=10, pady=5)

        self.get_button = tk.Button(self.main_frame, text="Get Password", command=self.get_password, height=1, width=10)
        self.get_button.pack(padx=10, pady=5)

        if self.password_set:
            self.show_frame(self.login_frame)
        else:
            self.show_frame(self.password_setup_frame)

    def generate_master_key(self):
        return Fernet.generate_key()

    def generate_key(self):
        self.key = Fernet.generate_key()
        return self.key

    def encrypt_password(self, password):
        f = Fernet(self.key)
        return f.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        return f.decrypt(encrypted_password.encode()).decode()

    passwords = {}

    def add_password(self):

        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if service and username and password:
            encrypted_password = self.encrypt_password(password)
            self.passwords[service] = {'username': username, 'password': encrypted_password}
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showwarning("Error", "Please fill in all the fields.")

    def get_password(self):
        self.service = self.service_entry.get()
        if self.service in self.passwords:
            encrypted_password = self.passwords[self.service]['password']
            decrypted_password = self.decrypt_password(encrypted_password)
            messagebox.showinfo("Password", f"Username: {self.passwords[self.service]['username']}\nPassword: {decrypted_password}")
        else:
            messagebox.showwarning("Error", "Password not found.")


    def check_password(self):
        try:
            with open("master_key.key", "rb") as master_key_file:
                self.key = master_key_file.read()

            with open("master_password.txt", "rb") as file:
                cipher_suite = Fernet(self.key)
                decrypted_password = cipher_suite.decrypt(file.read())
                self.password_set = bool(decrypted_password)
        except (FileNotFoundError, ValueError):
            self.password_set = False

    def encrypt_master_password(self, password):
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        return encrypted_password

    def show_frame(self, frame):
        # Hide all frames
        self.login_frame.pack_forget()
        self.password_setup_frame.pack_forget()
        self.main_frame.pack_forget()

        # Show the specified frame
        frame.pack()

    def check_login(self):
        entered_password = self.password_entry_login.get()

        try:
            with open("master_password.txt", "rb") as file:
                cipher_suite = Fernet(self.key)
                decrypted_password = cipher_suite.decrypt(file.read()).decode()

            if entered_password == decrypted_password:
                # Password is correct, show the main frame
                self.show_frame(self.main_frame)
            else:
                messagebox.showerror("Error", "Invalid password. Please try again.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Password not set. Set up a password first.")

    def save_password(self):
        self.key = self.generate_master_key()

        with open("master_key.key", "wb") as key_file:
            key_file.write(self.key)

        password = self.password_entry_setup.get()
        encrypted_password = self.encrypt_master_password(password)

        with open("master_password.txt", "wb") as file:
            file.write(encrypted_password)

        messagebox.showinfo("Success", "Password set successfully!")

        # Show the login frame after setting up the password
        self.show_frame(self.login_frame)

    def logout(self):
        # Clear the password entry field
        self.password_entry_login.delete(0, 'end')

        # Show the login frame after logout
        self.show_frame(self.login_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
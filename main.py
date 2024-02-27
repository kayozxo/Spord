import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Password App")
        self.root.geometry("300x200")

        self.password_set = False
        self.key = None

        # Check if password is set
        self.check_password()

        # Create login frame
        self.login_frame = tk.Frame(root)

        # Create widgets for login frame
        self.label_login = tk.Label(self.login_frame, text="Enter Password:", pady=10)
        self.label_login.pack()

        self.password_entry_login = tk.Entry(self.login_frame, show="*")
        self.password_entry_login.pack(pady=10)

        self.submit_button_login = tk.Button(self.login_frame, text="Login", command=self.check_login)
        self.submit_button_login.pack(pady=10)

        # Create password setup frame
        self.password_setup_frame = tk.Frame(root)

        # Create widgets for password setup frame
        self.label_setup = tk.Label(self.password_setup_frame, text="Set Password:", pady=10)
        self.label_setup.pack()

        self.password_entry_setup = tk.Entry(self.password_setup_frame, show="*")
        self.password_entry_setup.pack(pady=10)

        self.submit_button_setup = tk.Button(self.password_setup_frame, text="Submit", command=self.save_password)
        self.submit_button_setup.pack(pady=10)

        # Create main frame
        self.main_frame = tk.Frame(root)

        # Create widgets for main frame
        self.label_main = tk.Label(self.main_frame, text="Welcome to the App!", font=('Helvetica', 12), pady=20)
        self.label_main.pack()

        self.button_main = tk.Button(self.main_frame, text="Logout", command=self.logout)
        self.button_main.pack(pady=10)

        # Show the appropriate frame
        if self.password_set:
            self.show_frame(self.login_frame)
        else:
            self.show_frame(self.password_setup_frame)

    def generate_key(self):
        return Fernet.generate_key()

    def check_password(self):
        try:
            with open("key.key", "rb") as key_file:
                self.key = key_file.read()

            with open("password.txt", "rb") as file:
                cipher_suite = Fernet(self.key)
                decrypted_password = cipher_suite.decrypt(file.read())
                self.password_set = bool(decrypted_password)
        except (FileNotFoundError, ValueError):
            self.password_set = False

    def encrypt_password(self, password):
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
            with open("password.txt", "rb") as file:
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
        self.key = self.generate_key()

        with open("key.key", "wb") as key_file:
            key_file.write(self.key)

        password = self.password_entry_setup.get()
        encrypted_password = self.encrypt_password(password)

        with open("password.txt", "wb") as file:
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
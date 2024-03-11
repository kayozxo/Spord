import json, hashlib, getpass, os, sys
from cryptography.fernet import Fernet
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Password Manager")

        self.root.resizable(False, False)

        self.register_frame = ctk.CTkFrame(self.root, width=800, height=500, corner_radius=0)
        self.register_frame.pack()

        self.register_label = ctk.CTkLabel(self.register_frame, text="Register", font=("Roboto", 24))
        self.register_label.pack(pady=12, padx=10)

        self.register_username = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.register_username.pack(pady=12, padx=10)

        self.register_master_password = ctk.CTkEntry(self.register_frame, placeholder_text="Master Password", show="•")
        self.register_master_password.pack(pady=12, padx=10)

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register)
        self.register_button.pack(pady=12, padx=10)

        self.login_frame = ctk.CTkFrame(self.root, width=400, height=500, corner_radius=0)
        self.login_frame.pack(side="left", fill="both", expand=True)

        self.login_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Roboto", 24))
        self.login_label.pack(pady=12, padx=10)

        self.login_username = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.login_username.pack(pady=12, padx=10)

        self.login_master_password = ctk.CTkEntry(self.login_frame, placeholder_text="Master Password", show="•")
        self.login_master_password.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.main_frame = ctk.CTkFrame(self.root, width=400, height=500, corner_radius=0)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_label = ctk.CTkLabel(self.main_frame, text="Password Manager")
        self.main_label.pack(pady=12, padx=10)

        self.website = ctk.CTkEntry(self.main_frame, placeholder_text="Website Name")
        self.website.pack(pady=12, padx=10)

        self.password = ctk.CTkEntry(self.main_frame, placeholder_text="Password", show="•")
        self.password.pack(pady=12, padx=10)

        self.add_button = ctk.CTkButton(self.main_frame, text="Add", command=self.add_password)
        self.add_button.pack(pady=12, padx=10)

        self.view_button = ctk.CTkButton(self.main_frame, text="View", command=self.view_websites)
        self.view_button.pack(pady=12, padx=10)

        self.show_frame(self.register_frame)

        if os.path.exists('user_data.json') and os.path.getsize('user_data.json') != 0:
            self.show_frame(self.login_frame)
        else:
            self.show_frame(self.register_frame)


    def hash_password(self, password):
        sha256 = hashlib.sha256()
        sha256.update(password.encode())
        return sha256.hexdigest()

    def generate_key(self):
        return Fernet.generate_key()

    def initialize_cipher(self, key):
        return Fernet(key)

    def encrypt_password(self, cipher, password):
        return cipher.encrypt(password.encode()).decode()

    def decrypt_password(self, cipher, encrypted_password):
        return cipher.decrypt(encrypted_password.encode()).decode()

    def show_frame(self, frame):
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()

        frame.pack()

    def register(self):
        username = self.register_username.get()
        master_password = self.register_master_password.get()

        if username == '' or master_password == '':
            CTkMessagebox(title="Error", message="Please enter both username and master password")
        elif username == master_password:
            CTkMessagebox(title="Error", message="Username and master password cannot be the same")

        hashed_master_password = self.hash_password(master_password)
        user_data = {'username': username, 'master_password': hashed_master_password}
        file_name = 'user_data.json'
        if os.path.exists(file_name) and os.path.getsize(file_name) == 0:
            with open(file_name, 'w') as file:
                json.dump(user_data, file)
                CTkMessagebox(title="Info", message="Registration complete!!")
                self.show_frame(self.login_frame)
        else:
            with open(file_name, 'x') as file:
                json.dump(user_data, file)
                CTkMessagebox(title="Info", message="Registration complete!!")
                self.show_frame(self.login_frame)

        key_filename = 'encryption_key.key'
        if os.path.exists(key_filename):
            with open(key_filename, 'rb') as key_file:
                key = key_file.read()
        else:
            key = self.generate_key()
            with open(key_filename, 'wb') as key_file:
                key_file.write(key)

        self.cipher = self.initialize_cipher(key)

    def login(self):
        username = self.login_username.get()
        entered_password = self.login_master_password.get()

        try:
            with open('user_data.json', 'r') as file:
                user_data = json.load(file)
            stored_password_hash = user_data.get('master_password')
            entered_password_hash = self.hash_password(entered_password)
            if entered_password_hash == stored_password_hash and username == user_data.get('username'):
                CTkMessagebox(title="Success", icon="check", message="Login successful!!")
                self.show_frame(self.main_frame)
            else:
                CTkMessagebox(title="Error", icon="cancel", message="Invalid Login Credentials!")
        except Exception:
            CTkMessagebox(title="Error",icon="cancel", message="You have not registerd. Please Do That!")

    def view_websites(self):
        try:
            with open('passwords.json', 'r') as data:
                view = json.load(data)
                print("\nWebsites you saved...\n")
                for x in view:
                    print(x['website'])
                print('\n')
        except FileNotFoundError:
            print("\n[-] You have not saved any passwords!\n")

    def add_password(self):
        website = self.website.get()
        password = self.password.get()
        if not os.path.exists('passwords.json'):
            data = []
        else:
            try:
                with open('passwords.json', 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
        encrypted_password = self.encrypt_password(self.cipher, password)

        password_entry = {'website': website, 'password': encrypted_password}
        data.append(password_entry)

        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)

        CTkMessagebox(title="Success", icon="check", message="Password Added Successfully!!")

    def get_password(self, website):
        if not os.path.exists('passwords.json'):
            return None

        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['website'] == website:
                decrypted_password = self.decrypt_password(self.cipher, entry['password'])
                return decrypted_password
        return None

'''
while True:
   print("1. Register")
   print("2. Login")
   print("3. Quit")
   choice = input("Enter your choice: ")
   if choice == '1':
       file = 'user_data.json'
       if os.path.exists(file) and os.path.getsize(file) != 0:
           print("\n[-] Master user already exists!!")
           sys.exit()
       else:
           username = input("Enter your username: ")
           master_password = getpass.getpass("Enter your master password: ")
           register(username, master_password)
   elif choice == '2':
       file = 'user_data.json'
       if os.path.exists(file):
           username = input("Enter your username: ")
           master_password = getpass.getpass("Enter your master password: ")
           login(username, master_password)
       else:
           print("\n[-] You have not registered. Please do that.\n")
           sys.exit()

       while True:
           print("1. Add Password")
           print("2. Get Password")
           print("3. View Saved websites")
           print("4. Quit")
           password_choice = input("Enter your choice: ")
           if password_choice == '1':
               website = input("Enter website: ")
               password = getpass.getpass("Enter password: ")

               add_password(website, password)
               print("\n[+] Password added!\n")
           elif password_choice == '2':
               website = input("Enter website: ")
               decrypted_password = get_password(website)
               if website and decrypted_password:

                   print(f"\n[+] Password for {website}: {decrypted_password}\n[+] Password copied to clipboard.\n")
               else:
                   print("\n[-] Password not found! Did you save the password?"
                         "\n[-] Use option 3 to see the websites you saved.\n")
           elif password_choice == '3':
               view_websites()
           elif password_choice == '4':
               break
   elif choice == '3':
       break
'''

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

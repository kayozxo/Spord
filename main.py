import json, hashlib, os
from cryptography.fernet import Fernet
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Password Manager")
        self.root.configure(background='black')
        self.root.resizable(False, False)

        self.register_frame = ctk.CTkFrame(root, width=800, height=500)

        self.register_label = ctk.CTkLabel(self.register_frame, text="Register", font=("Montserrat Black", 24))
        self.register_label.place(x=400, y=50, anchor="center")

        self.register_username = ctk.CTkEntry(self.register_frame, placeholder_text="Username", width=250, height=40, font=("Montserrat", 12), corner_radius=5)
        self.register_username.place(x=400, y=140, anchor="center")

        self.register_master_password = ctk.CTkEntry(self.register_frame, placeholder_text="Master Password", show="•", width=250, height=40, corner_radius=5, font=("Montserrat", 12))
        self.register_master_password.place(x=400, y=190, anchor="center")

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.register_button.place(x=400, y=260, anchor="center")

        self.login_frame = ctk.CTkFrame(root, width=800, height=500)

        self.login_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Montserrat Black", 24))
        self.login_label.place(x=400, y=50, anchor="center")

        self.login_username = ctk.CTkEntry(self.login_frame, placeholder_text="Username", font=("Montserrat", 12), width=250, height=40, corner_radius=5)
        self.login_username.place(x=400, y=140, anchor="center")

        self.login_master_password = ctk.CTkEntry(self.login_frame, placeholder_text="Master Password", show="•", font=("Montserrat", 12), width=250, height=40, corner_radius=5)
        self.login_master_password.place(x=400, y=190, anchor="center")

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.login_button.place(x=400, y=260, anchor="center")

        self.main_frame = ctk.CTkFrame(root, width=800, height=500)

        self.main_label = ctk.CTkLabel(self.main_frame, text="Password Manager", font=("Montserrat Black", 24))
        self.main_label.place(x=400, y=50, anchor="center")

        self.website = ctk.CTkEntry(self.main_frame, placeholder_text="Website Name", font=("Montserrat", 12), width=250, height=40, corner_radius=5)
        self.website.place(x=400, y=120, anchor="center")

        self.password = ctk.CTkEntry(self.main_frame, placeholder_text="Enter Password", show="•", font=("Montserrat", 12), width=250, height=40, corner_radius=5)
        self.password.place(x=400, y=170, anchor="center")

        self.add_button = ctk.CTkButton(self.main_frame, text="Add Password", command=self.add_password, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.add_button.place(x=400, y=240, anchor="center")

        self.view_button = ctk.CTkButton(self.main_frame, text="View Websites", command=self.view_websites, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.view_button.place(x=400, y=300, anchor="center")

        self.get_password_button = ctk.CTkButton(self.main_frame, text="Get Password", command=self.get_password, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.get_password_button.place(x=400, y=360, anchor="center")

        self.how_label = ctk.CTkLabel(self.main_frame, text="To get a password, enter the website name and then click on 'Get Password' button", font=("Montserrat Light", 10))
        self.how_label.place(x=400, y=480, anchor="center")

        self.logout_button = ctk.CTkButton(self.main_frame, text="Logout", command=self.logout, font=("Montserrat Medium", 12), corner_radius=5, width=250, height=34)
        self.logout_button.place(x=400, y=420, anchor="center")

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
            CTkMessagebox(master=self.register_frame,title="Error",icon="warning.png", message="Please enter both username and master password", font=("Montserrat Medium", 12), icon_size=(40, 40))
        elif username == master_password:
            CTkMessagebox(master=self.register_frame,title="Error",icon="warning.png", message="Username and master password cannot be the same", font=("Montserrat Medium", 12), icon_size=(40, 40))
        else:
            hashed_master_password = self.hash_password(master_password)
            user_data = {'username': username, 'master_password': hashed_master_password}
            file_name = 'user_data.json'
            if os.path.exists(file_name) and os.path.getsize(file_name) == 0:
                with open(file_name, 'w') as file:
                    json.dump(user_data, file)
                    CTkMessagebox(master=self.register_frame,title="Success",icon="check.png", message="Registration complete!!", font=("Montserrat Medium", 12), icon_size=(40, 40))
                    self.show_frame(self.login_frame)
            else:
                with open(file_name, 'x') as file:
                    json.dump(user_data, file)
                    CTkMessagebox(master=self.register_frame,title="Success",icon="check.png", message="Registration complete!!", font=("Montserrat Medium", 12), icon_size=(40, 40))
                    self.show_frame(self.login_frame)

    def login(self):
        username = self.login_username.get()
        entered_password = self.login_master_password.get()

        try:
            with open('user_data.json', 'r') as file:
                user_data = json.load(file)
            stored_password_hash = user_data.get('master_password')
            entered_password_hash = self.hash_password(entered_password)
            if entered_password_hash == stored_password_hash and username == user_data.get('username'):
                CTkMessagebox(master=self.login_frame, title="Success", icon="check.png", message="Login successful!!", font=("Montserrat Medium", 12), corner_radius=10, icon_size=(40, 40))
                self.website.delete(0, 'end')
                self.password.delete(0, 'end')
                self.show_frame(self.main_frame)
            else:
                CTkMessagebox(master=self.login_frame,title="Error", icon="error.png", message="Invalid Login Credentials!", font=("Montserrat Medium", 12), icon_size=(40, 40))
        except Exception:
            CTkMessagebox(master=self.login_frame,title="Error",icon="error.png", message="You have not registered. Please Do That!", font=("Montserrat Medium", 12), icon_size=(40, 40))

        key_filename = 'encryption_key.key'
        if os.path.exists(key_filename):
            with open(key_filename, 'rb') as key_file:
                key = key_file.read()
        else:
            key = self.generate_key()
            with open(key_filename, 'wb') as key_file:
                key_file.write(key)

        self.cipher = self.initialize_cipher(key)

    def logout(self):
        self.show_frame(self.login_frame)
        self.login_username.delete(0, 'end')
        self.login_master_password.delete(0, 'end')


    def view_websites(self):
        try:
            with open('passwords.json', 'r') as data:
                view = json.load(data)
                CTkMessagebox(master=self.main_frame,icon="info.png",title="Websites", message='\n'.join(''.join(x['website'].upper()) for x in view), font=("Montserrat Medium", 12), icon_size=(40, 40))
        except FileNotFoundError:
            CTkMessagebox(master=self.main_frame,title="Error", icon="error.png", message="You have not saved any passwords!", font=("Montserrat Medium", 12), icon_size=(40, 40))

    def add_password(self):
        website = self.website.get()
        password = self.password.get()

        if website == "" or password == "":
            CTkMessagebox(master=self.main_frame,title="Error", icon="warning.png", message="Please enter both website and password!", font=("Montserrat Medium", 12), icon_size=(40, 40))
        else:
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

            CTkMessagebox(master=self.main_frame,title="Success", icon="check.png", message="Password Added Successfully!!", font=("Montserrat Medium", 12), icon_size=(40, 40))

    def get_password(self):
        website = self.website.get()
        if not os.path.exists('passwords.json'):
            CTkMessagebox(master=self.main_frame,title="error.png", icon="error.png", message="You have not saved any passwords!", font=("Montserrat Medium", 12), icon_size=(40, 40))
            return None

        if website == '':
            CTkMessagebox(master=self.main_frame,title="error.png", icon="warning.png", message="Please enter a website!", font=("Montserrat Medium", 12), icon_size=(40, 40))
            return None

        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        password_found = False

        for entry in data:
            if entry['website'] == website:
                decrypted_password = self.decrypt_password(self.cipher, entry['password'])
                CTkMessagebox(master=self.main_frame,icon="info.png", title="Password", message=f"Password For {website} : {decrypted_password}", font=("Montserrat Medium", 12), icon_size=(40, 40))
                password_found = True
                break

        if not password_found:
            CTkMessagebox(master=self.main_frame,title="Error", icon="error.png", message="Password Not Found!", font=("Montserrat Medium", 12), icon_size=(40, 40))

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
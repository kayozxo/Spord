import json, hashlib, getpass, os, sys
from cryptography.fernet import Fernet
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

def hash_password(password):
   sha256 = hashlib.sha256()
   sha256.update(password.encode())
   return sha256.hexdigest()

def generate_key():
   return Fernet.generate_key()

def initialize_cipher(key):
   return Fernet(key)

def encrypt_password(cipher, password):
   return cipher.encrypt(password.encode()).decode()

def decrypt_password(cipher, encrypted_password):
   return cipher.decrypt(encrypted_password.encode()).decode()

def register():
   file = 'user_data.json'
   if os.path.exists(file) and os.path.getsize(file) != 0:
           CTkMessagebox(title="Info", message="Master user already exists!!")
           sys.exit()
   else:
           username = register_username.get()
           master_password = register_master_password.get()
   hashed_master_password = hash_password(master_password)
   user_data = {'username': username, 'master_password': hashed_master_password}
   file_name = 'user_data.json'
   if os.path.exists(file_name) and os.path.getsize(file_name) == 0:
       with open(file_name, 'w') as file:
           json.dump(user_data, file)
           CTkMessagebox(title="Info", message="Registration complete!!")
   else:
       with open(file_name, 'x') as file:
           json.dump(user_data, file)
           CTkMessagebox(title="Info", message="Registration complete!!")

def login(username, entered_password):
   try:
       with open('user_data.json', 'r') as file:
           user_data = json.load(file)
       stored_password_hash = user_data.get('master_password')
       entered_password_hash = hash_password(entered_password)
       if entered_password_hash == stored_password_hash and username == user_data.get('username'):
           print("\n[+] Login Successful..\n")
       else:
           print("\n[-] Invalid Login credentials. Please use the credentials you used to register.\n")
           sys.exit()
   except Exception:
       print("\n[-] You have not registered. Please do that.\n")
       sys.exit()

def view_websites():
   try:
       with open('passwords.json', 'r') as data:
           view = json.load(data)
           print("\nWebsites you saved...\n")
           for x in view:
               print(x['website'])
           print('\n')
   except FileNotFoundError:
       print("\n[-] You have not saved any passwords!\n")

key_filename = 'encryption_key.key'
if os.path.exists(key_filename):
   with open(key_filename, 'rb') as key_file:
       key = key_file.read()
else:
   key = generate_key()
   with open(key_filename, 'wb') as key_file:
       key_file.write(key)

cipher = initialize_cipher(key)

def add_password(website, password):
   if not os.path.exists('passwords.json'):
       data = []
   else:
       try:
           with open('passwords.json', 'r') as file:
               data = json.load(file)
       except json.JSONDecodeError:
           data = []
   encrypted_password = encrypt_password(cipher, password)

   password_entry = {'website': website, 'password': encrypted_password}
   data.append(password_entry)

   with open('passwords.json', 'w') as file:
       json.dump(data, file, indent=4)

def get_password(website):

   if not os.path.exists('passwords.json'):
       return None

   try:
       with open('passwords.json', 'r') as file:
           data = json.load(file)
   except json.JSONDecodeError:
       data = []

   for entry in data:
       if entry['website'] == website:
           decrypted_password = decrypt_password(cipher, entry['password'])
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

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

app = ctk.CTk()
app.geometry("800x500")
app.title("Password Manager")

app.resizable(False, False)

register_frame = ctk.CTkFrame(app, width=400, height=500, corner_radius=0)
register_frame.pack(side="right", fill="both", expand=True)

register_username = ctk.CTkEntry(register_frame, placeholder_text="Username")
register_username.pack(pady=12, padx=10)

register_master_password = ctk.CTkEntry(register_frame, placeholder_text="Master Password", show="•")
register_master_password.pack(pady=12, padx=10)

register_button = ctk.CTkButton(register_frame, text="Register", command=register)
register_button.pack(pady=12, padx=10)

login_frame = ctk.CTkFrame(app, width=400, height=500, corner_radius=0)
login_frame.pack(side="left", fill="both", expand=True)

login_username = ctk.CTkEntry(login_frame, placeholder_text="Username")
login_username.pack(pady=12, padx=10)

login_master_password = ctk.CTkEntry(login_frame, placeholder_text="Master Password", show="•")
login_master_password.pack(pady=12, padx=10)

login_button = ctk.CTkButton(login_frame, text="Login", command=lambda: login(login_username.get(), login_master_password.get()))
login_button.pack(pady=12, padx=10)

main_frame = ctk.CTkFrame(app, width=400, height=500, corner_radius=0)
main_frame.pack(side="top", fill="both", expand=True)

main_label = ctk.CTkLabel(main_frame, text="Password Manager")
main_label.pack(pady=12, padx=10)

app.mainloop()
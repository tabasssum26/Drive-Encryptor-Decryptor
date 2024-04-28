import tkinter as tk
from tkinter import ttk, filedialog
import pyAesCrypt
import os
import pyttsx3

BUFFER_SIZE = 80 * 1080


def encrypt_drive(password):
    status_label.config(text="Please wait a few seconds", fg="blue")
    folder_selected = filedialog.askdirectory()
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            file_path = os.path.join(root, file)
            encrypted_file_path = file_path + ".aes"
            pyAesCrypt.encryptFile(file_path, encrypted_file_path, password, BUFFER_SIZE)
            os.remove(file_path)
    speak("Please wait a few seconds")

    status_label.config(text="Drive Encrypted Successfully", fg="yellow")
    speak("Drive Encrypted Successfully")

def decrypt_drive(password):
    status_label.config(text="Please wait a few seconds", fg="blue")
    folder_selected = filedialog.askdirectory()
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith(".aes"):
                encrypted_file_path = os.path.join(root, file)
                decrypted_file_path = encrypted_file_path[:-4]
                pyAesCrypt.decryptFile(encrypted_file_path, decrypted_file_path, password, BUFFER_SIZE)
                os.remove(encrypted_file_path)


    speak("Please wait a few seconds")
    status_label.config(text="Drive Decrypted Successfully", fg="green")

    speak("Drive Decrypted Successfully")

def update_button_color(button, color):
    style = ttk.Style()
    style.configure(button, background=color)

def encrypt_decrypt_gui():
    root = tk.Tk()
    root.title("Drive Encryptor/Decryptor")
    root.geometry("400x200")
    root.config(bg="black")

    # Load the background image
    background_image = tk.PhotoImage(file="Untitled design.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="Created By Tabassum", bg="black", fg="white", font=("Helvetica", 12, "bold"))
    title_label.pack(side="top", pady=5)

    speak("Welcome to Encryptor & Decryptor ")

    def encrypt():
        password = password_entry.get()
        encrypt_drive(password)

    def decrypt():
        password = password_entry.get()
        decrypt_drive(password)

    password_label = tk.Label(root, text="Enter Password:", bg="black", fg="white", font=("Helvetica", 12))
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5)

    encrypt_button = ttk.Button(root, text="Encrypt Drive", command=encrypt, style="TButton")
    encrypt_button.pack(pady=5)
    update_button_color("TButton", "sky blue")

    decrypt_button = ttk.Button(root, text="Decrypt Drive", command=decrypt, style="TButton")
    decrypt_button.pack(pady=5)
    update_button_color("TButton", "sky blue")

    global status_label
    status_label = tk.Label(root, text="", bg="black", fg="green", font=("Helvetica", 12, "bold"))
    status_label.pack(pady=5)

    root.mainloop()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    voices = engine.getProperty('voices')
    # Selecting a female voice
    female_voice = None
    for voice in voices:
        if "female" in voice.name.lower():
            female_voice = voice
            break
    if female_voice:
        engine.setProperty('voice', female_voice.id)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    encrypt_decrypt_gui()

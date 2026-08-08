from tkinter import *
from PIL import Image, ImageTk
from admin_login import admin
from user_login import user
root = Tk()
root.title("Smart Health Assistance System")
root.geometry("1450x900")
root.config(bg="#ADD1EF")
def open_admin():
    root.withdraw()
    admin(root)
def open_user():
    root.withdraw()
    user(root)
def on_close():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
# Heading
Label(
    root,
    text="Welcome",
    font=("Arial", 32, "bold"),
    fg="#0D47A1",
    bg="#B2D9E0"
).place(relx=0.5, rely=0.12, anchor=CENTER)
Label(
    root,
    text="Smart Health Assistance System",
    font=("Arial", 18),
    fg="#1565C0",
    bg="#B2D9E0"
).place(relx=0.5, rely=0.20, anchor=CENTER)
# Logo
img = Image.open("logo.png")
img = img.resize((120, 120))
photo = ImageTk.PhotoImage(img)
logo = Label(root, image=photo, bg="#E3F2FD")
logo.image = photo
logo.place(relx=0.5, rely=0.33, anchor=CENTER)
Button(
    root,
    text="Admin Login",
    font=("Arial", 15, "bold"),
    bg="#212121",
    fg="white",
    padx=25,
    pady=12,
    command=open_admin
).place(relx=0.35, rely=0.60, anchor=CENTER)
Button(
    root,
    text="User Login",
    font=("Arial", 15, "bold"),
    bg="#212121",
    fg="white",
    padx=25,
    pady=12,
    command=open_user
).place(relx=0.65, rely=0.60, anchor=CENTER)
root.mainloop()
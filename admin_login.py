from tkinter import *
from tkinter import messagebox
import mysql.connector
from admin_dashboard import admin_dashboard
def admin(parent):
    root = Toplevel(parent)
    root.title("Admin Login")
    root.geometry("700x500")
    root.config(bg="#90CAF9")
    def close_window():
        parent.deiconify()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", close_window)
    Label(
        root,
        text="Admin Login",
        font=("Arial", 28, "bold"),
        bg="#90CAF9",
        fg="#0D47A1"
    ).pack(pady=20)
    # Username
    Label(
        root,
        text="Username",
        font=("Arial", 14),
        bg="#90CAF9"
    ).pack()
    username = Entry(
        root,
        width=30,
        font=("Arial", 14)
    )
    username.pack(pady=5)
    # Password
    Label(
        root,
        text="Password",
        font=("Arial", 14),
        bg="#90CAF9"
    ).pack()
    password = Entry(
        root,
        width=30,
        show="*",
        font=("Arial", 14)
    )
    password.pack(pady=5)
    # ---------------- Database Connection ----------------
    def get_connection():

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="diseasedb"
        )
    # ---------------- Login ----------------
    def login():
        if username.get().strip() == "" or password.get().strip() == "":
            messagebox.showerror(
                "Error",
                "Please enter Username and Password",
                parent=root
            )
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT id, username
            FROM admins
            WHERE username=%s AND password=%s
            """
            cursor.execute(
                query,
                (
                    username.get().strip(),
                    password.get().strip()
                )
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            print(result)
            if result:
                admin_data = {
                    "id": result[0],
                    "username": result[1]
                }
                messagebox.showinfo(
                    "Success",
                    "Login Successful",
                    parent=root
                )
                root.destroy()
                admin_dashboard(parent, admin_data)
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid Username or Password",
                    parent=root
                )
        except mysql.connector.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=root
            )
    Button(
        root,
        text="Login",
        font=("Arial", 14, "bold"),
        bg="#0D47A1",
        fg="white",
        width=15,
        command=login
    ).pack(pady=25)
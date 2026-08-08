from tkinter import *
from tkinter import ttk
import mysql.connector
def admin_dashboard(parent, admin_data):
    root = Toplevel(parent)
    root.title("Admin Dashboard")
    root.geometry("1200x650")
    root.config(bg="#E3F2FD")
    def close_window():
        parent.deiconify()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", close_window)
    Label(
        root,
        text="Disease Prediction System",
        font=("Arial", 24, "bold"),
        fg="#0D47A1",
        bg="#E3F2FD"
    ).pack(pady=10)
    Label(
        root,
        text=f"Welcome Admin : {admin_data['username']}",
        font=("Arial", 15),
        bg="#E3F2FD"
    ).pack()
    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Phone",
        "Email",
        "Location",
        "Username"
    )
    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=20
    )
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(fill=BOTH, expand=True, padx=20, pady=20)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="diseasedb"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
        id,
        full_name,
        age,
        gender,
        phone,
        email,
        location,
        username
        FROM users
    """)
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", END, values=row)
    cursor.close()
    conn.close()
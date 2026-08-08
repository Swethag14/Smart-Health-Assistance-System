from tkinter import *
from tkinter import messagebox
import mysql.connector
from symptom_page import symptom_page
from tkinter import ttk
from password_validator import validate_password
def user(parent):
    root = Toplevel(parent)
    root.title("User Login")
    root.geometry("700x550")
    root.config(bg="#90CAF9")
    def close_window():
        parent.deiconify()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", close_window)
    Label(
        root,
        text="User Login",
        font=("Arial", 28, "bold"),
        bg="#90CAF9"
    ).pack(pady=20)
    Label(root, text="Username",
          bg="#90CAF9",
          font=("Arial", 14)).pack()
    username = Entry(root, width=30, font=("Arial", 14))
    username.pack(pady=5)
    Label(root, text="Password",
          bg="#90CAF9",
          font=("Arial", 14)).pack()
    password = Entry(root, width=30,
                     show="*",
                     font=("Arial", 14))
    password.pack(pady=5)
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="diseasedb"
        )
    def login():
        print("Login button clicked")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
            SELECT id,
                full_name,
                age,
                gender,
                phone,
                email,
                location,
                pincode,
                username
            FROM users
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
            print("Database Result:", result)
            cursor.close()
            conn.close()
            if result:
                user_data = {
                    "id": result[0],
                    "full_name": result[1],
                    "age": result[2],
                    "gender": result[3],
                    "phone": result[4],
                    "email": result[5],
                    "location": result[6],
                    "pincode":result[7],
                    "username": result[8],
                }
                messagebox.showinfo(
                    "Success",
                    f"Welcome {user_data['full_name']}!",
                    parent=root
                )
                root.destroy()
                symptom_page(parent, user_data)
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
    def register():
        reg = Toplevel(root)
        reg.title("User Registration")
        reg.geometry("550x700")
        reg.config(bg="#E3F2FD")
        Label(
            reg,
            text="User Registration",
            font=("Arial",22,"bold"),
            bg="#E3F2FD",
            fg="#0D47A1"
        ).pack(pady=15)
        # Full Name
        Label(reg,text="Full Name",bg="#E3F2FD").pack()
        fullname = Entry(reg,width=35,font=("Arial",12))
        fullname.pack(pady=5)
        # Age
        Label(reg,text="Age",bg="#E3F2FD").pack()
        age = Entry(reg,width=35,font=("Arial",12))
        age.pack(pady=5)
        # Gender
        Label(reg,text="Gender",bg="#E3F2FD").pack()
        gender = ttk.Combobox(
            reg,
            values=["Male","Female","Other"],
            state="readonly",
            width=32
        )
        gender.pack(pady=5)
        gender.current(0)
        # Phone
        Label(reg,text="Phone Number",bg="#E3F2FD").pack()
        phone = Entry(reg,width=35,font=("Arial",12))
        phone.pack(pady=5)
        # Email
        Label(reg,text="Email",bg="#E3F2FD").pack()
        email = Entry(reg,width=35,font=("Arial",12))
        email.pack(pady=5)
        # Location
        Label(reg,text="Location (City)",bg="#E3F2FD").pack()
        location = Entry(reg,width=35,font=("Arial",12))
        location.pack(pady=5)
        #Pincode
        Label(reg,text="Pincode (Area)",bg="#E3F2FD").pack()
        pincode = Entry(reg,width=35,font=("Arial",12))
        pincode.pack(pady=5)
        # Username
        Label(reg,text="Username",bg="#E3F2FD").pack()
        new_user = Entry(reg,width=35,font=("Arial",12))
        new_user.pack(pady=5)
        # Password
        Label(reg,text="Password",bg="#E3F2FD").pack()
        new_pwd = Entry(reg,width=35,show="*",font=("Arial",12))
        new_pwd.pack(pady=5)
        pwd_hint = Label(
            reg,
            text="Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char",
            bg="#E3F2FD",
            fg="#4B5A63",
            font=("Arial", 9)
        )
        pwd_hint.pack()
        # Confirm Password
        Label(reg,text="Confirm Password",bg="#E3F2FD").pack()
        confirm = Entry(reg,width=35,show="*",font=("Arial",12))
        confirm.pack(pady=5)
        def save():
            if (
                fullname.get().strip()=="" or
                age.get().strip()=="" or
                phone.get().strip()=="" or
                email.get().strip()=="" or
                location.get().strip()=="" or
                pincode.get().strip()=="" or
                new_user.get().strip()=="" or
                new_pwd.get()=="" or
                confirm.get()==""
            ):
                messagebox.showerror(
                    "Error",
                    "Please fill all fields.",
                    parent=reg
                )
                return
            # ---- Password strength check (before the match check, so the
            #      user gets the strength error first if both are weak) ----
            valid, message = validate_password(new_pwd.get())
            if not valid:
                messagebox.showerror(
                    "Weak Password",
                    message,
                    parent=reg
                )
                return
            if new_pwd.get() != confirm.get():
                messagebox.showerror(
                    "Error",
                    "Passwords do not match.",
                    parent=reg
                )
                return
            # Validate Age
            try:
                age_value = int(age.get().strip())
                if age_value <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please enter a valid age.",
                    parent=reg
                )
                return
            # Validate Phone
            if not phone.get().strip().isdigit() or len(phone.get().strip()) != 10:
                messagebox.showerror(
                    "Error",
                    "Enter a valid 10-digit phone number.",
                    parent=reg
                )
                return
            # Validate Email
            if "@" not in email.get() or "." not in email.get():
                messagebox.showerror(
                    "Error",
                    "Enter a valid email address.",
                    parent=reg
                )
                return
            if pincode.get().strip() == "":
                messagebox.showerror(
                    "Error",
                    "Please enter your pincode."
                )
                return
            if not pincode.get().isdigit() or len(pincode.get()) != 6:
                messagebox.showerror(
                    "Error",
                    "Enter a valid 6-digit pincode."
                )
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                query = """
                INSERT INTO users
                (
                    full_name,
                    age,
                    gender,
                    phone,
                    email,
                    location,
                    pincode,
                    username,
                    password
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(
                    query,
                    (
                        fullname.get().strip(),
                        age_value,
                        gender.get(),
                        phone.get().strip(),
                        email.get().strip(),
                        location.get().strip(),
                        pincode.get().strip(),
                        new_user.get().strip(),
                        new_pwd.get()
                    )
                )
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "Registration Successful!",
                    parent=reg
                )
                reg.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror(
                    "Error",
                    "Username already exists.",
                    parent=reg
                )
            except mysql.connector.Error as e:
                messagebox.showerror(
                    "Database Error",
                    str(e),
                    parent=reg
                )
            finally:
                cursor.close()
                conn.close()
        Button(
            reg,
            text="Register",
            bg="#0D47A1",
            fg="white",
            font=("Arial",13,"bold"),
            command=save
        ).pack(pady=20)
    # ---------------- Main Buttons ----------------
    Button(
        root,
        text="Login",
        font=("Arial",13,"bold"),
        bg="#0D47A1",
        fg="white",
        command=login
    ).pack(pady=15)
    Button(
        root,
        text="Register",
        font=("Arial",13,"bold"),
        bg="green",
        fg="white",
        command=register
    ).pack(pady=5)
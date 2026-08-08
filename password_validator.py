"""
password_validator.py
----------------------
Reusable password strength validation for the Smart Health Assistance
System (Registration / Reset Password screens).

Rules enforced:
  - At least 8 characters
  - At least 1 uppercase letter        (A-Z)
  - At least 1 lowercase letter        (a-z)
  - At least 1 digit                   (0-9)
  - At least 1 special character       (!@#$%^&* etc.)
  - No spaces
"""

import re
from tkinter import *

# ---------------- Palette (matches result_page.py) ----------------
CARD_BG   = "#FFFFFF"
OK_FG     = "#00695C"    # dark teal  - requirement met
OK_BG     = "#E0F2F1"    # light teal
FAIL_FG   = "#8D2F2F"    # dark red   - requirement not met
FAIL_BG   = "#FCEBEB"    # light red
NEUTRAL_FG = "#4B5A63"


# ==========================================================
# Core validation function - use this anywhere (no UI needed)
# ==========================================================
def validate_password(password: str):
    """
    Validates a password against standard strength rules.

    Returns:
        (True, "Password is strong.")                if valid
        (False, "<first rule that failed>")           if invalid
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if re.search(r'\s', password):
        return False, "Password must not contain spaces."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=~`\[\]\\/;\']', password):
        return False, "Password must contain at least one special character."
    return True, "Password is strong."


def password_rules_status(password: str):
    """
    Returns a dict of {rule_label: True/False} for every individual rule,
    useful for a live checklist UI (see PasswordChecklist below).
    """
    return {
        "At least 8 characters":      len(password) >= 8,
        "One uppercase letter (A-Z)": bool(re.search(r'[A-Z]', password)),
        "One lowercase letter (a-z)": bool(re.search(r'[a-z]', password)),
        "One digit (0-9)":            bool(re.search(r'[0-9]', password)),
        "One special character":      bool(re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=~`\[\]\\/;\']', password)),
        "No spaces":                  password != "" and not re.search(r'\s', password),
    }


# ==========================================================
# Optional Tkinter widget - a live requirements checklist
# that updates in green/red as the user types
# ==========================================================
class PasswordChecklist(Frame):
    """
    Drop this under a password Entry field. Call `.update_status(password)`
    on every <KeyRelease> of the Entry to refresh the checklist live.

    Example:
        pwd_entry = Entry(parent, show="*")
        pwd_entry.pack()

        checklist = PasswordChecklist(parent)
        checklist.pack(pady=(6, 0))

        pwd_entry.bind(
            "<KeyRelease>",
            lambda e: checklist.update_status(pwd_entry.get())
        )
    """
    def __init__(self, parent, bg=CARD_BG):
        super().__init__(parent, bg=bg)
        self.bg = bg
        self.labels = {}
        rules = password_rules_status("")  # just to get the rule labels/order
        for rule in rules:
            lbl = Label(
                self,
                text="○  " + rule,
                font=("Arial", 10),
                fg=NEUTRAL_FG,
                bg=bg,
                anchor="w",
                justify=LEFT
            )
            lbl.pack(fill=X, padx=10, pady=1)
            self.labels[rule] = lbl

    def update_status(self, password: str):
        status = password_rules_status(password)
        for rule, passed in status.items():
            lbl = self.labels[rule]
            if passed:
                lbl.config(text="✔  " + rule, fg=OK_FG, bg=OK_BG)
            else:
                lbl.config(text="○  " + rule, fg=FAIL_FG, bg=FAIL_BG)

    def all_passed(self, password: str) -> bool:
        return all(password_rules_status(password).values())


# ==========================================================
# Example: wiring this into a "Set / Reset Password" screen
# ==========================================================
def set_password_screen(parent, on_success):
    """
    A minimal standalone Set Password screen. `on_success(new_password)`
    is called once a valid, matching password is confirmed.
    """
    win = Toplevel(parent)
    win.title("Set New Password")
    win.config(bg=CARD_BG)
    win.geometry("420x420")

    Label(
        win, text="Set New Password", font=("Arial", 16, "bold"),
        fg="#0D47A1", bg=CARD_BG
    ).pack(pady=(20, 10))

    Label(win, text="New Password", font=("Arial", 11), bg=CARD_BG).pack(pady=(10, 2))
    pwd_entry = Entry(win, show="*", font=("Arial", 12), justify=CENTER, width=28)
    pwd_entry.pack(pady=2)

    checklist = PasswordChecklist(win)
    checklist.pack(pady=(10, 10), padx=20, fill=X)

    Label(win, text="Confirm Password", font=("Arial", 11), bg=CARD_BG).pack(pady=(10, 2))
    confirm_entry = Entry(win, show="*", font=("Arial", 12), justify=CENTER, width=28)
    confirm_entry.pack(pady=2)

    status_label = Label(win, text="", font=("Arial", 10, "bold"), bg=CARD_BG)
    status_label.pack(pady=10)

    def on_key_release(event=None):
        checklist.update_status(pwd_entry.get())

    pwd_entry.bind("<KeyRelease>", on_key_release)

    def submit():
        pwd = pwd_entry.get()
        confirm = confirm_entry.get()

        valid, message = validate_password(pwd)
        if not valid:
            status_label.config(text=message, fg=FAIL_FG)
            return
        if pwd != confirm:
            status_label.config(text="Passwords do not match.", fg=FAIL_FG)
            return

        status_label.config(text="Password set successfully!", fg=OK_FG)
        win.after(800, win.destroy)
        on_success(pwd)

    Button(
        win, text="Save Password", font=("Arial", 12, "bold"),
        bg="#1565C0", fg="white", padx=15, pady=6,
        cursor="hand2", command=submit
    ).pack(pady=15)

    return win


if __name__ == "__main__":
    # Quick manual test without any UI
    for test_pwd in ["short", "alllowercase1!", "NoDigits!!", "NoSpecialChar1", "Valid@Pass1"]:
        ok, msg = validate_password(test_pwd)
        print(f"{test_pwd!r:20} -> {ok} | {msg}")
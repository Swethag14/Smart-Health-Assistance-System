from data import suggestions, hospital_data
import webbrowser
from urllib.parse import quote
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import *
from tkinter import messagebox, filedialog

# ---------------- Shared color palette (blue -> teal healthcare theme) ----------------
BG          = "#EAF4FB"   # page background
CARD_BG     = "#FFFFFF"   # neutral white cards
BORDER      = "#BBDEFB"   # soft blue border accent
HEADING_FG  = "#0D47A1"   # deep blue - main heading
SUBHEAD_FG  = "#1565C0"   # blue - section subheadings
ACCENT_BG   = "#E3F2FD"   # light blue panel (disease card)
ACCENT_TXT  = "#0D47A1"   # deep blue text on light blue
ALERT_FG    = "#C62828"   # muted red - disease name (kept as an alert accent)
ALERT_SUB   = "#8D2F2F"   # deep red - severity text
PATIENT_BG  = "#E8EAF6"   # light indigo panel (patient details)
PATIENT_FG  = "#283593"   # deep indigo text on light indigo
SYMPTOM_BG  = "#E0F7FA"   # light cyan panel (symptoms)
SYMPTOM_FG  = "#00838F"   # deep cyan text on light cyan
TEAL_BG     = "#E0F2F1"   # soft teal panel (suggestions)
TEAL_FG     = "#00695C"   # teal text
INFO_BG     = "#E1ECFB"   # light blue panel (hospitals)
INFO_FG     = "#0D47A1"   # deep blue text
MUTED_FG    = "#4B5A63"   # muted gray-blue for timestamps

# How far left (in px) to nudge the centered content column off dead-center
LEFT_SHIFT  = 60

def result_page(parent, user_data, disease, selected_symptoms):
    root = Toplevel(parent)
    root.title("Disease Prediction Result")
    root.config(bg=BG)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")
    root.resizable(True, True)
# ---------------- Scrollable Window ----------------
    container = Frame(root, bg=BG)
    container.pack(fill=BOTH, expand=True)
    canvas = Canvas(
        container,
        bg=BG,
        highlightthickness=0
    )
    scrollbar = Scrollbar(
        container,
        orient=VERTICAL,
        command=canvas.yview
    )
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    main_frame = Frame(canvas, bg=BG)
    canvas_window = canvas.create_window(
        (0, 0),
        window=main_frame,
        anchor="n"
    )
    main_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    # Keep the content column centered (with a slight left nudge) as the window resizes
    canvas.bind(
        "<Configure>",
        lambda e: canvas.coords(canvas_window, e.width // 2 - LEFT_SHIFT, 0)
    )
    def close_window():
        parent.deiconify()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", close_window)
    # ---------------- Heading ----------------
    Label(
        main_frame,
        text="Disease Prediction Result",
        font=("Arial", 24, "bold"),
        fg=HEADING_FG,
        bg=BG
    ).pack(pady=(20,16))
    # ================= Patient Details =================
    details = Frame(
            main_frame,
            bg=PATIENT_BG,
            bd=2,
            relief=RIDGE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
    details.pack(
            fill=X,
            padx=20,
            pady=12
        )
    Label(
            details,
            text="👤 Patient Details",
            font=("Arial",15,"bold"),
            fg=PATIENT_FG,
            bg=PATIENT_BG
        ).pack(pady=(14,10))
    info_frame = Frame(details, bg=PATIENT_BG)
    info_frame.pack(pady=(0,16))
    info_frame.grid_columnconfigure(0, weight=1)
    info_frame.grid_columnconfigure(1, weight=1)
    Label(
            info_frame,
            text=f"Name : {user_data['full_name']}",
            font=("Arial",11),
            fg=PATIENT_FG,
            bg=PATIENT_BG
        ).grid(row=0,column=0,padx=40,pady=6)
    Label(
            info_frame,
            text=f"Age : {user_data['age']}",
            font=("Arial",11),
            fg=PATIENT_FG,
            bg=PATIENT_BG
        ).grid(row=0,column=1,padx=40,pady=6)
    Label(
            info_frame,
            text=f"Gender : {user_data['gender']}",
            font=("Arial",11),
            fg=PATIENT_FG,
            bg=PATIENT_BG
        ).grid(row=1,column=0,padx=40,pady=6)
    Label(
            info_frame,
            text=f"Location : {user_data['location']}",
            font=("Arial",11),
            fg=PATIENT_FG,
            bg=PATIENT_BG
        ).grid(row=1,column=1,padx=40,pady=6)
    Label(
        info_frame,
        text=f"Pincode : {user_data['pincode']}",
        font=("Arial",11),
        fg=PATIENT_FG,
        bg=PATIENT_BG
    ).grid(row=2,column=0,columnspan=2,pady=6)
    # ---------------- Severity ----------------
    severity = {
        "Allergy": "Low",
        "Common Cold": "Low",
        "GERD": "Low",
        "Migraine": "Medium",
        "Typhoid": "High",
        "Pneumonia": "High",
        "Dengue": "High",
        "Malaria": "High",
        "Heart Attack": "Critical",
        "Hypertension": "Medium"
    }
    level = severity.get(disease, "Medium")
    # Row 1 (Disease + Symptoms)
    row1 = Frame(main_frame, bg=BG)
    row1.pack(fill=X, padx=20, pady=(0,4))
    # ================= Disease =================
    disease_frame = Frame(
        row1,
        bg=ACCENT_BG,
        bd=2,
        relief=RIDGE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    disease_frame.pack(
        side=LEFT,
        fill=BOTH,
        expand=True,
        padx=(0,10)
    )
    Label(
        disease_frame,
        text="🩺 Predicted Disease",
        font=("Arial",16,"bold"),
        fg=ACCENT_TXT,
        bg=ACCENT_BG
    ).pack(pady=(16,10))
    Label(
        disease_frame,
        text=disease,
        font=("Arial",20,"bold"),
        fg=ALERT_FG,
        bg=ACCENT_BG
    ).pack(pady=8)
    Label(
        disease_frame,
        text=f"Severity : {level}",
        font=("Arial",12,"bold"),
        fg=ALERT_SUB,
        bg=ACCENT_BG
    ).pack(pady=(8,16))
    # ================= Symptoms =================
    symptom_frame = Frame(
        row1,
        bg=SYMPTOM_BG,
        bd=2,
        relief=RIDGE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    symptom_frame.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )
    Label(
        symptom_frame,
        text="📝 Selected Symptoms",
        font=("Arial",15,"bold"),
        fg=SYMPTOM_FG,
        bg=SYMPTOM_BG
    ).pack(pady=(16,10))
    for symptom in selected_symptoms:
        Label(
            symptom_frame,
            text=symptom.replace("_"," ").title(),
            font=("Arial",11),
            fg=SYMPTOM_FG,
            bg=SYMPTOM_BG,
            justify=CENTER,
            anchor="center"
        ).pack(fill=X, padx=20, pady=4)
    Label(symptom_frame, text="", bg=SYMPTOM_BG).pack(pady=2)  # bottom breathing room
     # Row 2 (Suggestions)
    suggestion_frame = Frame(
        main_frame,
        bg=TEAL_BG,
        bd=2,
        relief=RIDGE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    suggestion_frame.pack(
        fill=X,
        padx=20,
        pady=14
    )
    Label(
        suggestion_frame,
        text="💡 Health Suggestions",
        font=("Arial",15,"bold"),
        fg=TEAL_FG,
        bg=TEAL_BG
    ).pack(pady=(16,10))
    disease_suggestions = suggestions.get(
        disease,
        ["Please consult a doctor."]
    )
    for item in disease_suggestions:
        Label(
            suggestion_frame,
            text="✔ " + item,
            font=("Arial",11),
            fg=TEAL_FG,
            bg=TEAL_BG,
            justify=CENTER,
            wraplength=700,
            anchor="center"
        ).pack(fill=X, padx=20, pady=4)
    Label(suggestion_frame, text="", bg=TEAL_BG).pack(pady=2)  # bottom breathing room
    # Nearby Hospitals
    hospital_frame = Frame(
        main_frame,
        bg=INFO_BG,
        bd=2,
        relief=RIDGE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    hospital_frame.pack(
        fill=X,
        padx=20,
        pady=14
    )
    Label(
        hospital_frame,
        text="🏥 Nearby Hospitals",
        font=("Arial",15,"bold"),
        fg=INFO_FG,
        bg=INFO_BG
    ).pack(pady=(16,10))
    location = user_data["location"].strip().title()
    hospitals = hospital_data.get(
        location,
        ["No hospitals found for this location."]
    )
    for hospital in hospitals:
        Label(
            hospital_frame,
            text="🏥 " + hospital,
            font=("Arial",11),
            fg=INFO_FG,
            bg=INFO_BG,
            justify=CENTER,
            anchor="center"
        ).pack(
            fill=X,
            padx=20,
            pady=4
        )
    def show_nearby_hospitals():
        pincode = user_data["pincode"]
        query = quote(f"Hospitals near {pincode}")
        url = f"https://www.google.com/maps/search/{query}"
        webbrowser.open(url)
    Button(
        hospital_frame,
        text="📍 Show Nearby Hospitals on Google Maps",
        font=("Arial",12,"bold"),
        bg=SUBHEAD_FG,
        fg="white",
        cursor="hand2",
        padx=15,
        pady=6,
        command=show_nearby_hospitals
    ).pack(pady=(14,18))
    # Generated Date & Time
    Label(
        main_frame,
        text=f"Report Generated : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}",
        font=("Arial",10,"italic"),
        fg=MUTED_FG,
        bg=BG
    ).pack(pady=(10,8))
    def export_pdf():
        file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Report"
        )
        if not file:
            return
        doc = SimpleDocTemplate(file)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("<b>Disease Prediction Report</b>", styles["Title"]))
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph(f"<b>Name:</b> {user_data['full_name']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Age:</b> {user_data['age']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Gender:</b> {user_data['gender']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Location:</b> {user_data['location']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Pincode:</b> {user_data['pincode']}", styles["Normal"]))
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph(f"<b>Predicted Disease:</b> {disease}", styles["Heading2"]))
        story.append(Paragraph(f"<b>Severity:</b> {level}", styles["Normal"]))
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph("<b>Selected Symptoms</b>", styles["Heading2"]))
        for symptom in selected_symptoms:
            story.append(
                Paragraph("• " + symptom.replace("_", " ").title(), styles["Normal"])
            )
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph("<b>Suggestions</b>", styles["Heading2"]))
        for item in disease_suggestions:
            story.append(
                Paragraph("• " + item, styles["Normal"])
            )
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph("<b>Nearby Hospitals</b>", styles["Heading2"]))
        for hospital in hospitals:
            story.append(
                Paragraph("• " + hospital, styles["Normal"])
            )
        story.append(Paragraph("<br/>", styles["Normal"]))
        story.append(Paragraph(
            "<i>Disclaimer: This prediction is generated by an automated "
            "Machine Learning model and is intended for informational "
            "purposes only. It is NOT a medical diagnosis. Please consult "
            "a qualified healthcare professional before making any "
            "medical decisions.</i>",
            styles["Normal"]
        ))
        doc.build(story)
    button_frame = Frame(main_frame, bg=BG)
    button_frame.pack(pady=(15,30))
    Button(
        button_frame,
        text="📄 Export Report",
        font=("Arial",12,"bold"),
        bg=TEAL_FG,
        fg="white",
        padx=18,
        pady=8,
        command=export_pdf,
        cursor="hand2"
    ).pack(side=LEFT, padx=14)
    Button(
        button_frame,
        text="❌ Close",
        font=("Arial",12,"bold"),
        bg=HEADING_FG,
        fg="white",
        padx=18,
        pady=8,
        command=close_window,
        cursor="hand2"
    ).pack(side=LEFT, padx=14)

    # ---------------- Disclaimer ----------------
    disclaimer = Frame(main_frame, bg=BG)
    disclaimer.pack(fill=X, padx=40, pady=(0, 24))
    Label(
        disclaimer,
        text=(
            "⚠ Disclaimer: This prediction is generated by an automated "
            "Machine Learning model and is intended for informational "
            "purposes only. It is NOT a medical diagnosis. Please consult "
            "a qualified healthcare professional before making any "
            "medical decisions."
        ),
        font=("Arial", 9, "italic"),
        fg=MUTED_FG,
        bg=BG,
        justify=CENTER,
        wraplength=700
    ).pack()

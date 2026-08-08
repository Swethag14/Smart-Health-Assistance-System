from tkinter import *
from tkinter import messagebox
from predict import predict_disease
from tkinter import ttk
from result_page import result_page
# Symptoms from the Kaggle dataset
SYMPTOMS = [
    "itching",
    "skin_rash",
    "nodal_skin_eruptions",
    "continuous_sneezing",
    "shivering",
    "chills",
    "joint_pain",
    "stomach_pain",
    "acidity",
    "ulcers_on_tongue",
    "muscle_wasting",
    "vomiting",
    "burning_micturition",
    "spotting_urination",
    "fatigue",
    "weight_gain",
    "anxiety",
    "cold_hands_and_feets",
    "mood_swings",
    "weight_loss",
    "restlessness",
    "lethargy",
    "patches_in_throat",
    "irregular_sugar_level",
    "cough",
    "high_fever",
    "sunken_eyes",
    "breathlessness",
    "sweating",
    "dehydration",
    "indigestion",
    "headache",
    "yellowish_skin",
    "dark_urine",
    "nausea",
    "loss_of_appetite",
    "pain_behind_the_eyes",
    "back_pain",
    "constipation",
    "abdominal_pain",
    "diarrhoea",
    "mild_fever",
    "yellow_urine",
    "yellowing_of_eyes",
    "acute_liver_failure",
    "fluid_overload",
    "swelling_of_stomach",
    "swelled_lymph_nodes",
    "malaise",
    "blurred_and_distorted_vision",
    "phlegm",
    "throat_irritation",
    "redness_of_eyes",
    "sinus_pressure",
    "runny_nose",
    "congestion",
    "chest_pain",
    "weakness_of_limbs",
    "fast_heart_rate",
    "pain_during_bowel_movements",
    "pain_in_anal_region",
    "bloody_stool",
    "irritation_in_anus",
    "neck_pain",
    "dizziness",
    "cramps",
    "bruising",
    "obesity",
    "swollen_legs",
    "swollen_blood_vessels",
    "puffy_face_and_eyes",
    "enlarged_thyroid",
    "brittle_nails",
    "swollen_extremeties",
    "excessive_hunger",
    "drying_and_tingling_lips",
    "slurred_speech",
    "knee_pain",
    "hip_joint_pain",
    "muscle_weakness",
    "stiff_neck",
    "swelling_joints",
    "movement_stiffness",
    "spinning_movements",
    "loss_of_balance",
    "unsteadiness",
    "weakness_of_one_body_side",
    "loss_of_smell",
    "bladder_discomfort",
    "foul_smell_of_urine",
    "continuous_feel_of_urine",
    "passage_of_gases",
    "internal_itching",
    "toxic_look_typhos",
    "depression",
    "irritability",
    "muscle_pain",
    "altered_sensorium",
    "red_spots_over_body",
    "belly_pain",
    "abnormal_menstruation",
    "dischromic_patches",
    "watering_from_eyes",
    "increased_appetite",
    "polyuria",
    "family_history",
    "mucoid_sputum",
    "rusty_sputum",
    "lack_of_concentration",
    "visual_disturbances",
    "receiving_blood_transfusion",
    "receiving_unsterile_injections",
    "coma",
    "stomach_bleeding",
    "distention_of_abdomen",
    "history_of_alcohol_consumption",
    "blood_in_sputum",
    "prominent_veins_on_calf",
    "palpitations",
    "painful_walking",
    "pus_filled_pimples",
    "blackheads",
    "scurring",
    "skin_peeling",
    "silver_like_dusting",
    "small_dents_in_nails",
    "inflammatory_nails",
    "blister",
    "red_sore_around_nose",
    "yellow_crust_ooze"
]
def symptom_page(parent,user_data):
    root = Toplevel(parent)
    root.geometry("1000x750")
    root.title("Health Assessment")
    root.config(bg="#E3F2FD")
    # ---------------- Heading ----------------
    Label(
        root,
        text="Health Assessment",
        font=("Arial", 30, "bold"),
        fg="#0D47A1",
        bg="#E3F2FD"
    ).pack(pady=(20, 5))
    Label(
        root,
        text="Please answer the following questions about your symptoms",
        font=("Arial", 14),
        fg="#1565C0",
        bg="#E3F2FD"
    ).pack(pady=(0, 15))
    # ---------------- Duration ----------------
    duration_frame = Frame(root, bg="#E3F2FD")
    duration_frame.pack(pady=10)
    Label(
        duration_frame,
        text="How many days have you had these symptoms?",
        font=("Arial", 14, "bold"),
        bg="#E3F2FD"
    ).pack(side=LEFT, padx=10)
    duration_entry = Entry(
        duration_frame,
        width=10,
        font=("Arial", 13)
    )
    duration_entry.pack(side=LEFT)
    Label(
        duration_frame,
        text="days",
        font=("Arial", 13),
        bg="#E3F2FD"
    ).pack(side=LEFT, padx=5)
    # ---------------- Welcome User ----------------
    Label(
        root,
        text=f"Welcome, {user_data['full_name']}",
        font=("Arial", 16, "bold"),
        fg="green",
        bg="#E3F2FD"
    ).pack(pady=20)
    # ---------------- Symptom Selection -------------
    search_frame = Frame(root, bg="#E3F2FD")
    search_frame.pack(fill=X, padx=20, pady=10)
    Label(
        search_frame,
        text="🔍 Search Symptom",
        font=("Arial", 13, "bold"),
        bg="#E3F2FD"
    ).pack(side=LEFT, padx=10)
    search_var = StringVar()
    search_entry = Entry(
        search_frame,
        textvariable=search_var,
        width=40,
        font=("Arial", 12)
    )
    search_entry.pack(side=LEFT, padx=10)
    # Scrollable Area
    container = Frame(root, bg="#E3F2FD")
    container.pack(fill=BOTH, expand=True, padx=30, pady=10)
    canvas = Canvas(
        container,
        bg="white",
        highlightthickness=0
    )
    scrollbar = Scrollbar(
        container,
        orient=VERTICAL,
        command=canvas.yview
    )
    symptom_frame = Frame(
        canvas,
        bg="white"
    )
    symptom_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window(
        (0, 0),
        window=symptom_frame,
        anchor="nw",
        width=900
    )
    canvas.configure(
        yscrollcommand=scrollbar.set
    )
    canvas.pack(
        side=LEFT,
        fill=BOTH,
        expand=True
    )
    scrollbar.pack(
        side=RIGHT,
        fill=Y
    )
    # Symptoms
    symptom_vars = {}
    rows = []
    for symptom in SYMPTOMS:
        var = IntVar(value=0)
        symptom_vars[symptom] = var
        row = Frame(
            symptom_frame,
            bg="white"
        )
        display_name = symptom.replace("_", " ").title()
        Label(
            row,
            text=f"Do you have {display_name}?",
            font=("Arial", 12),
            bg="white",
            anchor="w",
            width=45
        ).pack(
            side=LEFT,
            padx=10
        )
        Radiobutton(
            row,
            text="Yes",
            variable=var,
            value=1,
            bg="white",
            font=("Arial", 11)
        ).pack(
            side=LEFT,
            padx=10
        )
        Radiobutton(
            row,
            text="No",
            variable=var,
            value=0,
            bg="white",
            font=("Arial", 11)
        ).pack(
            side=LEFT,
            padx=10
        )
        row.pack(
            fill=X,
            padx=20,
            pady=4
        )
        rows.append((symptom, row))
    # Search Function
    def filter_symptoms(*args):
        keyword = search_var.get().lower().strip()
        # Hide all rows
        for symptom, row in rows:
            row.pack_forget()
        # Show only matching rows
        for symptom, row in rows:
            symptom_name = symptom.replace("_", " ").lower()
            if keyword == "" or keyword in symptom_name:
                row.pack(
                    fill=X,
                    padx=20,
                    pady=4
                )
    # Call whenever user types
    search_var.trace_add("write", filter_symptoms)
# Predict Disease
    def submit_symptoms():
        duration = duration_entry.get().strip()
        if duration == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter symptom duration."
            )
            return
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number of days."
            )
            return
        selected_symptoms = []
        for symptom, var in symptom_vars.items():
            if var.get() == 1:
                selected_symptoms.append(symptom)
        if len(selected_symptoms) == 0:
            messagebox.showwarning(
                "No Symptoms",
                "Please select at least one symptom."
            )
            return
        disease = predict_disease(selected_symptoms)
        result_page(
            parent,
            user_data,
            disease,
            selected_symptoms
        )
    # ---------------- Button ----------------
    Button(
        root,
        text="Predict Disease",
        font=("Arial",15,"bold"),
        bg="#0D47A1",
        fg="white",
        padx=35,
        pady=12,
        command=submit_symptoms
    ).pack(pady=20)
    
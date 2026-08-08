Smart Health Assistance System 🏥
📌 Overview

The Smart Health Assistance System is a Python and Machine Learning-based application designed for preliminary disease assessment. Users can select their symptoms, receive a possible disease prediction with severity level, view health suggestions, find nearby hospitals using their pincode, and export the prediction results as a PDF report.

✨ Features
User registration and secure login
Admin login and dashboard
Searchable symptom selection
Machine Learning-based disease prediction
Disease severity prediction
Health suggestions and precautions
Nearby hospital search using pincode
Google Maps integration
PDF report generation
MySQL database for storing user and prediction data
Input validation and error handling
User-friendly Tkinter interface
🛠️ Technologies Used
Python
Tkinter – GUI
Machine Learning – Disease prediction
MySQL – Database
ReportLab – PDF report generation
Google Maps – Nearby hospital search

📂 Project Structure

Disease Prediction/
│
├── main.py
├── app.py
├── welcome_page.py
├── user_login.py
├── registration.py
├── admin_login.py
├── admin_dashboard.py
├── symptom_page.py
├── result_page.py
├── predict.py
├── model.py
├── train_model.py
├── database.py
├── data.py
├── requirements.txt
└── README.md

⚙️ Installation

Clone the repository:

git clone <your-github-repository-link>
cd Disease-Prediction

Install the required packages:

pip install -r requirements.txt

Configure your MySQL database and update the database credentials in database.py.

▶️ Run the Project
python main.py
🔄 System Workflow
Welcome Page
     ↓
Registration / Login
     ↓
Health Assessment
     ↓
Search & Select Symptoms
     ↓
Machine Learning Prediction
     ↓
Disease + Severity + Suggestions
     ↓
Nearby Hospitals
     ↓
Export PDF Report

⚠️ Disclaimer

This system is intended for preliminary health assessment and educational purposes only. Disease predictions should not be considered a medical diagnosis. Users should consult a qualified healthcare professional for proper diagnosis and treatment.

👩‍💻 Developed By

Swetha Ganeshkumar

import streamlit as st
import pandas as pd
import joblib

model = joblib.load("best_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Diabetes Prediction")

gender = st.selectbox("Gender", [0,1,2])

age = st.number_input("Age", min_value=1.0, max_value=100.0)

location = st.number_input("Location Code", min_value=0, max_value=54)

race = st.selectbox(
    "Race",
    [
        "AfricanAmerican",
        "Asian",
        "Caucasian",
        "Hispanic",
        "Other"
    ]
)

hypertension = st.selectbox("Hypertension", [0,1])

heart_disease = st.selectbox("Heart Disease", [0,1])

smoking_history = st.selectbox(
    "Smoking History",
    [0,1,2,3,4,5]
)

bmi = st.number_input(
    "BMI",
    min_value=10.0,
    max_value=60.0
)

hba1c = st.number_input(
    "HbA1c Level",
    min_value=1.0,
    max_value=15.0
)

glucose = st.number_input(
    "Blood Glucose Level",
    min_value=50.0,
    max_value=400.0
)

if st.button("Predict"):

    if age <= 30:
        age_group = 2
    elif age <= 60:
        age_group = 0
    else:
        age_group = 1

    if bmi < 18.5:
        bmi_category = 3
    elif bmi < 25:
        bmi_category = 0
    elif bmi < 30:
        bmi_category = 2
    else:
        bmi_category = 1

    high_glucose = 1 if glucose >= 126 else 0
    high_hba1c = 1 if hba1c >= 6.5 else 0

    risk_score = (
        hypertension
        + heart_disease
        + high_glucose
        + high_hba1c
    )

    race_african = 1 if race == "AfricanAmerican" else 0
    race_asian = 1 if race == "Asian" else 0
    race_caucasian = 1 if race == "Caucasian" else 0
    race_hispanic = 1 if race == "Hispanic" else 0
    race_other = 1 if race == "Other" else 0

    data = pd.DataFrame([{
        'gender': gender,
        'age': age,
        'location': location,
        'race:AfricanAmerican': race_african,
        'race:Asian': race_asian,
        'race:Caucasian': race_caucasian,
        'race:Hispanic': race_hispanic,
        'race:Other': race_other,
        'hypertension': hypertension,
        'heart_disease': heart_disease,
        'smoking_history': smoking_history,
        'bmi': bmi,
        'hbA1c_level': hba1c,
        'blood_glucose_level': glucose,
        'age_group': age_group,
        'bmi_category': bmi_category,
        'high_glucose': high_glucose,
        'high_hba1c': high_hba1c,
        'risk_score': risk_score
    }])

    num_cols = [
        'age',
        'bmi',
        'hbA1c_level',
        'blood_glucose_level'
    ]

    data[num_cols] = scaler.transform(
        data[num_cols]
    )

    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("High Risk of Diabetes")
    else:
        st.success("Low Risk of Diabetes")
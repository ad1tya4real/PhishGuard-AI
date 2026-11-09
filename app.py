
import streamlit as st
import joblib
import os
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# Load ML model
model_path = "model/phishing_model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Design
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
}
h1, h2, h3, p, label {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ PhishGuard AI")
st.subheader("Intelligent Phishing Email Detection System")
st.write("Analyze suspicious emails using Machine Learning.")

st.divider()

# Dashboard
col1, col2 = st.columns(2)

with col1:
    st.metric("Detection Engine", "Active" if model else "Offline")

with col2:
    st.metric("Security Status", "Ready" if model else "Model Missing")

st.divider()

# Email input
st.header("📧 Email Analysis")

email = st.text_area(
    "Paste email content below:",
    height=180,
    placeholder="Paste your suspicious email here..."
)

keywords = [
    "urgent", "verify your account", "password",
    "free prize", "click here", "bank details",
    "claim your reward", "account suspended",
    "lottery", "won a prize", "immediately"
]

if st.button("🔍 Analyze Email", use_container_width=True):

    if not email.strip():
        st.warning("Please enter an email.")

    elif model is None:
        st.error("Model not found. Train your model first.")

    else:
        prediction = model.predict([email])[0]

        risk_score = 0

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba([email])[0]
            classes = list(model.classes_)

            phishing_index = next(
                (i for i, c in enumerate(classes)
                 if str(c).lower() in ["1", "phishing"]),
                None
            )

            if phishing_index is not None:
                risk_score = round(
                    probabilities[phishing_index] * 100
                )

        is_phishing = str(prediction).lower() in ["1", "phishing"]

        found_keywords = [
            word for word in keywords
            if word in email.lower()
        ]

        # Save analysis
        history_file = "analysis_history.csv"

        record = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Email": email,
            "Prediction": "Phishing" if is_phishing else "Legitimate",
            "Risk Score": risk_score
        }])

        record.to_csv(
            history_file,
            mode="a",
            header=not os.path.exists(history_file) or os.path.getsize(history_file) == 0,
            index=False
        )

        st.divider()
        st.header("📊 Analysis Report")

        result_col, risk_col = st.columns(2)

        with result_col:
            st.subheader("AI Prediction")

            if is_phishing:
                st.error("⚠️ Possible Phishing Email")
            else:
                st.success("✅ Appears Legitimate")

        with risk_col:
            st.subheader("ML Risk Indicator")
            st.progress(risk_score / 100)
            st.write(f"Risk Score: {risk_score}/100")

            if risk_score >= 70:
                st.error("High Risk")
            elif risk_score >= 40:
                st.warning("Medium Risk")
            else:
                st.success("Low Risk")

        st.subheader("🔎 Suspicious Indicators")

        if found_keywords:
            for word in found_keywords:
                st.warning(f"Suspicious phrase detected: {word}")
        else:
            st.info("No configured suspicious phrases detected.")

        st.caption(
            "Educational demonstration only. "
            "A low score does not guarantee an email is safe."
        )

# Detection History
st.divider()
st.header("📚 Detection History")

if os.path.exists("analysis_history.csv"):
    try:
        history = pd.read_csv("analysis_history.csv")

        if not history.empty:
            total = len(history)
            phishing = len(history[history["Prediction"] == "Phishing"])
            legitimate = len(history[history["Prediction"] == "Legitimate"])

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Scanned", total)
            col2.metric("Phishing Detected", phishing)
            col3.metric("Legitimate Emails", legitimate)

            st.subheader("Previous Email Analyses")
            st.dataframe(history, use_container_width=True)

            st.download_button(
                "📥 Download Analysis History",
                history.to_csv(index=False),
                "phishguard_history.csv",
                "text/csv"
            )
        else:
            st.info("No analysis history available yet.")

    except Exception:
        st.info("No analysis history available yet.")
else:
    st.info("No analysis history available yet.")

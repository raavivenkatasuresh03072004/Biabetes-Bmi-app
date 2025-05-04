import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from streamlit_lottie import st_lottie
import json
import base64

# Function to load Lottie animations from a local file
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Function to set background image using base64
def set_bg_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image
set_bg_image("assets/Black.jpg")  # Ensure this path is correct

# Function to animate title letters (falling animation)
def animated_title(title):
    return ''.join([f'<span class="fall-down">{letter}</span>' for letter in title])

# App title with animation
st.markdown(
    f"""
    <style>
    /* Title animation */
    .title-animation {{
        text-align: center;
        font-size: 3em;
        font-weight: bold;
    }}
    .fall-down {{
        display: inline-block;
        opacity: 0;
        transform: translateY(-50px);
        animation: fall 1s forwards;
    }}

    /* Animation for falling effect */
    @keyframes fall {{
        0% {{
            opacity: 0;
            transform: translateY(-50px);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* Apply a delay to each letter to make them fall one by one */
    .fall-down:nth-child(1) {{
        animation-delay: 0.2s;
    }}
    .fall-down:nth-child(2) {{
        animation-delay: 0.4s;
    }}
    .fall-down:nth-child(3) {{
        animation-delay: 0.6s;
    }}
    .fall-down:nth-child(4) {{
        animation-delay: 0.8s;
    }}
    .fall-down:nth-child(5) {{
        animation-delay: 1s;
    }}
    .fall-down:nth-child(6) {{
        animation-delay: 1.2s;
    }}
    .fall-down:nth-child(7) {{
        animation-delay: 1.4s;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title with falling animation
st.markdown(
    f"<h1 class='title-animation'>{animated_title('🩺 DIABETIES   PREDICTION   APP')}</h1>",
    unsafe_allow_html=True
)
# Load model
model = joblib.load('svm_model.pkl')        

# Load and display Lottie animation
lottie_json = load_lottie_file("assets/Doctor_Animation.json")
st_lottie(lottie_json, speed=1, width=700, height=400, key="animation", loop=True, quality="high")

# Input fields
st.header("📋 Enter Patient Details")
age = st.number_input("Age", min_value=1, max_value=120, value=25)
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0)
skin_thickness = st.number_input("Skin Thickness", min_value=1.0, max_value=100.0, value=20.0)

if st.button("🔍 Predict"):
    input_data = np.array([[age, bmi, skin_thickness]])
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("🧸 Prediction: Diabetic")
        with st.expander("🔍 Suggestions for Diabetic Patients"):
            st.markdown("- 🥗 **Maintain a healthy, low-sugar diet** (rich in vegetables and whole grains).")
            st.markdown("- 🏃 **Exercise daily** – even walking 30 minutes helps.")
            st.markdown("- 🧪 **Monitor your blood sugar** regularly.")
            st.markdown("- 💊 **Follow prescribed medication or insulin plans.**")
            st.markdown("- 🧺 **Schedule regular checkups** with your healthcare provider.")
    else:
        st.success("✅ Prediction: Not Diabetic")
        with st.expander("💡 Tips to Stay Healthy and Prevent Diabetes"):
            st.markdown("- 🍎 **Eat a balanced diet** (limit processed foods and sugary drinks).")
            st.markdown("- 🏃‍♂️ **Stay physically active** – at least 150 minutes of exercise per week.")
            st.markdown("- ⚖️ **Maintain a healthy weight.**")
            st.markdown("- 🚭 **Avoid smoking and excess alcohol.**")
            st.markdown("- 🦡 **Get regular screening if you’re at risk.**")

# BMI Calculator
st.header("⚖️ BMI Calculator")
height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0, value=170.0)
weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0, value=70.0)

if st.button("📐 Calculate BMI"):
    height_m = height / 100
    bmi_result = round(weight / (height_m ** 2), 2)

    if bmi_result < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi_result < 24.9:
        category = "Normal weight"
    elif 25 <= bmi_result < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"

    st.info(f"Your BMI is {bmi_result} ({category})")

    # BMI Bar Chart
    st.subheader("📊 BMI Category Chart")
    bmi_categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
    bmi_ranges = [18.5, 24.9, 29.9, 40]
    colors = ['#74c0fc', '#51cf66', '#fcc419', '#ff6b6b']

    fig, ax = plt.subplots()
    ax.bar(bmi_categories, bmi_ranges, color=colors, alpha=0.7, zorder=2)
    ax.axhline(bmi_result, color='black', linewidth=2, linestyle='--', label=f'Your BMI: {bmi_result}')
    ax.set_ylabel("BMI Value")
    ax.set_title("BMI Categories")
    ax.legend()
    st.pyplot(fig)

    # BMI Gauge
    st.subheader("🎯 BMI Gauge Indicator")
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.axis('off')
    angles = [0, 45, 90, 135, 180]
    colors_arc = ['#74c0fc', '#51cf66', '#fcc419', '#ff6b6b']

    for i in range(4):
        ax2.add_patch(Wedge((0.5, 0), 0.4, 180 - angles[i+1], 180 - angles[i],
                            facecolor=colors_arc[i], transform=ax2.transAxes))

    needle_angle = min(bmi_result, 40) * 4.5
    ax2.annotate('▼', xy=(0.5 + 0.3 * np.cos(np.radians(needle_angle + 180)),
                          0.3 + 0.3 * np.sin(np.radians(needle_angle + 180))),
                 fontsize=24, ha='center', va='center', color='black')
    ax2.set_title("BMI Dial (0–40 Scale)", fontsize=12)
    st.pyplot(fig2)

    # BMI Pie Chart
    st.subheader("🥧 BMI Risk Chart")
    if category == 'Normal weight':
        healthy = 1
        risk = 0
    elif category == "Underweight":
        healthy = 0.2
        risk = 0.8
    elif category == "Overweight":
        healthy = 0.4
        risk = 0.6
    else:
        healthy = 0.1
        risk = 0.9

    fig3, ax3 = plt.subplots()
    ax3.pie([healthy, risk], labels=['Healthy Zone', 'Risk Zone'],
            colors=['#51cf66', '#ff6b6b'], autopct='%1.0f%%',
            startangle=90, textprops={'fontsize': 12})
    ax3.axis('equal')
    st.pyplot(fig3)









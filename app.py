import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
import langchain.globals as lcg

# Load environment variables
load_dotenv()
lcg.set_verbose(True)

# Model Setup
config = {"temperature": 0.6, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = GoogleGenerativeAI(model="gemini-1.5-flash", config=config)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=['name', 'age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'state', 'allergics', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurant names, 6 breakfast names, 5 dinner names, and 6 workout names, "
             "based on the following criteria:\n"
             "Person name: {name}\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person state: {state}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)

# Runnable Chain
chain_resto = RunnableLambda(lambda inputs: prompt_template.format(**inputs)) | model

# Usage Tracking
usage_data = []
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = []

# Custom Styling
def apply_styling():
    st.markdown(
        """
        <style>
            .title {
                font-size: 32px;
                font-weight: bold;
                font-family: 'Arial', sans-serif;
                text-align: center;
                color: #FFFFFF;
                margin-bottom: 20px;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px;
                border-radius: 10px;
            }
            .subtitle {
                font-size: 20px;
                font-family: 'Helvetica', sans-serif;
                text-align: center;
                color: #FFFFFF;
                margin-bottom: 30px;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px;
                border-radius: 10px;
            }
            .form-label {
                font-weight: bold;
                color: #FFFFFF;
            }
            .form-input {
                margin-bottom: 15px;
            }
            .recommendations {
                margin-top: 20px;
                font-family: 'Helvetica', sans-serif;
            }
            .bmi {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
                margin-top: 10px;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px;
                border-radius: 10px;
            }
            .stButton button {
                transition: background-color 0.3s, transform 0.3s;
            }
            .stButton button:hover {
                background-color: #4CAF50;
                transform: scale(1.05);
            }
            .form-container {
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Usage Tracking Functions
def capture_usage():
    st.session_state.timestamp.append(datetime.now())
    usage_data.append({'timestamp': st.session_state.timestamp[-1]})

def create_usage_graph():
    start_date = date(2024, 1, 1)
    end_date = date.today()
    date_range = pd.date_range(start_date, end_date, freq='W-MON')
    weeks = [d.strftime("%Y-%m-%d") for d in date_range]
    usage_count = [10, 20, 15, 25, 30, 5, 10, 8, 15, 18, 8, 15, 10, 20, 22]  # Placeholder

    fig = go.Figure(data=[go.Bar(x=weeks, y=usage_count, text=usage_count, textposition='auto')])
    fig.update_layout(title='Weekly Usage Tracking', xaxis_title='Week', yaxis_title='Usage Count')
    st.plotly_chart(fig)

# BMI Calculation and Visualization
def calculate_bmi(weight, height):
    height_m = float(height) / 100.0
    return float(weight) / (height_m ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 24.9:
        return 'Normal weight'
    elif 25 <= bmi < 29.9:
        return 'Overweight'
    return 'Obesity'

def visualize_bmi(age, weight, bmi, category):
    bmi_colors = {'Underweight': 'blue', 'Normal weight': 'green', 'Overweight': 'yellow', 'Obesity': 'red'}
    color = bmi_colors[category]

    fig = go.Figure(data=[go.Scatter3d(
        x=[int(age)], y=[float(weight)], z=[bmi],
        mode='markers',
        marker=dict(size=12, color=color, opacity=0.8),
        text=[f"Age: {age}<br>Weight: {weight} kg<br>BMI: {bmi:.2f}<br>Category: {category}"],
        hoverinfo='text'
    )])

    fig.update_layout(
        title='3D BMI Visualization',
        scene=dict(
            xaxis_title='Age', yaxis_title='Weight (kg)', zaxis_title='BMI',
            xaxis=dict(backgroundcolor="rgb(200, 200, 230)", gridcolor="white", showbackground=True, zerolinecolor="white"),
            yaxis=dict(backgroundcolor="rgb(230, 200,230)", gridcolor="white", showbackground=True, zerolinecolor="white"),
            zaxis=dict(backgroundcolor="rgb(230, 230,200)", gridcolor="white", showbackground=True, zerolinecolor="white"),
        ),
        margin=dict(r=10, l=10, b=10, t=30)
    )
    st.plotly_chart(fig)
    st.markdown(f'<div class="bmi">Your BMI is {bmi:.2f}, which falls under the category: {category}</div>', unsafe_allow_html=True)

# Main App
def main():
    apply_styling()
    st.markdown('<div class="title">FitBro: Personalized Diet & Workout Plans</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Tailored recommendations for your health goals</div>', unsafe_allow_html=True)

    with st.form(key='user_input_form', clear_on_submit=True):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<div class="form-label">Name:</div>', unsafe_allow_html=True)
        name = st.text_input('Name', placeholder='Enter your name', label_visibility='hidden')

        st.markdown('<div class="form-label">Age:</div>', unsafe_allow_html=True)
        age = st.text_input('Age', placeholder='Enter your age', label_visibility='hidden')

        st.markdown('<div class="form-label">Gender:</div>', unsafe_allow_html=True)
        gender = st.selectbox('Gender', ['Male', 'Female'], label_visibility='hidden')

        st.markdown('<div class="form-label">Weight (kg):</div>', unsafe_allow_html=True)
        weight = st.text_input('Weight (kg)', placeholder='Enter your weight in kg', label_visibility='hidden')

        st.markdown('<div class="form-label">Height (cm):</div>', unsafe_allow_html=True)
        height = st.text_input('Height (cm)', placeholder='Enter your height in cm', label_visibility='hidden')

        st.markdown('<div class="form-label">Veg or Non-Veg:</div>', unsafe_allow_html=True)
        veg_or_nonveg = st.selectbox('Veg or Non-Veg', ['Veg', 'Non-Veg'], label_visibility='hidden')

        st.markdown('<div class="form-label">Disease:</div>', unsafe_allow_html=True)
        disease = st.text_input('Disease', placeholder='Enter any generic disease', label_visibility='hidden')

        st.markdown('<div class="form-label">Region:</div>', unsafe_allow_html=True)
        region = st.text_input('Region', placeholder='Enter your region', label_visibility='hidden')

        st.markdown('<div class="form-label">State:</div>', unsafe_allow_html=True)
        state = st.text_input('State', placeholder='Enter your state', label_visibility='hidden')

        st.markdown('<div class="form-label">Allergics:</div>', unsafe_allow_html=True)
        allergics = st.text_input('Allergics', placeholder='Enter any allergies', label_visibility='hidden')

        st.markdown('<div class="form-label">Food Type:</div>', unsafe_allow_html=True)
        foodtype = st.text_input('Food Type', placeholder='Enter your preferred food type', label_visibility='hidden')

        submit_button = st.form_submit_button(label='Get Recommendations')
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if all([name, age, gender, weight, height, veg_or_nonveg, disease, region, state, allergics, foodtype]):
            input_data = {
                'name': name, 'age': age, 'gender': gender, 'weight': weight, 'height': height,
                'veg_or_nonveg': veg_or_nonveg, 'disease': disease, 'region': region, 'state': state,
                'allergics': allergics, 'foodtype': foodtype
            }
            capture_usage()
            recommendations = chain_resto.invoke(input_data)
            st.markdown('<div class="subtitle">Recommendations:</div>', unsafe_allow_html=True)
            st.markdown('<div class="recommendations">', unsafe_allow_html=True)
            st.markdown(recommendations, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            bmi = calculate_bmi(weight, height)
            category = categorize_bmi(bmi)
            visualize_bmi(age, weight, bmi, category)
        else:
            st.error("Please fill in all the form fields.")

    st.markdown('<div class="subtitle">Weekly Usage Tracking</div>', unsafe_allow_html=True)
    create_usage_graph()

if __name__ == "__main__":
    main()
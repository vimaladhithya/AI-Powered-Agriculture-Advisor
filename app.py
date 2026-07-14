import streamlit as st
import google.generativeai as genai
from agents.location_agent import run_location_agent
from agents.weather_agent import run_weather_agent
from agents.soil_agent import run_soil_agent
from agents.agriculture_agent import run_agriculture_agent
import pandas as pd

# PAGE CONFIG

st.set_page_config(
    page_title="🌱 AI Agro Advisor",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS

st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

/* Hero Banner */
.hero{
    background: linear-gradient(135deg,#16a34a,#22c55e);
    padding:35px;
    border-radius:25px;
    text-align:center;
    color:white;
    box-shadow:0px 8px 25px rgba(0,0,0,0.4);
    margin-bottom:25px;
}

/* Glass Cards */
.metric-card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    border:1px solid rgba(255,255,255,0.15);
    box-shadow:0px 8px 25px rgba(0,0,0,0.25);
    transition:0.3s;
}

.metric-card:hover{
    transform:translateY(-8px);
}

/* Result Boxes */
.result-box{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding:20px;
    border-radius:20px;
    border-left:5px solid #22c55e;
    margin-bottom:15px;
    color:white;
    box-shadow:0px 8px 20px rgba(0,0,0,0.25);
}

/* Button */
.stButton > button{
    width:100%;
    height:55px;
    border-radius:15px;
    background:#22c55e;
    color:white;
    font-size:18px;
    font-weight:bold;
}

/* Input */
.stTextInput input{
    border-radius:15px;
}

/* Rain Animation */
.rain{
    font-size:45px;
    animation: rain 1s infinite alternate;
}

@keyframes rain{
    from {transform: translateY(-8px);}
    to {transform: translateY(10px);}
}

</style>
""", unsafe_allow_html=True)

# GEMINI CONFIG

API_KEY=st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

models = [
    model.name
    for model in genai.list_models()
]


st.markdown("""
<div class="hero">
<h1>🌱 AI Powered Agriculture Advisor</h1>
<h3>Smart Farming using AI, Weather & Soil Intelligence</h3>
</div>
""", unsafe_allow_html=True)

# ANIMATED RAIN

st.markdown("""
<center>
<div class='rain'>
🌧️ 🌧️ 🌧️ 🌧️ 🌧️
</div>
</center>
""", unsafe_allow_html=True)

# SIDEBAR

with st.sidebar:

    st.title("🚜 Agro Dashboard")

    selected_model = st.selectbox(
        "Select Gemini Model",
        models
    )

    selected_model = selected_model.replace(
        "models/",
        "gemini/"
    )

    st.markdown("---")

    

    st.success("📍 Location Insights")
    st.info("🌦 Weather Intelligence")
    st.warning("🌱 Soil Analysis")
    st.success("🌾 Crop Recommendation")

# FARMER / TRACTOR / CROPS

st.subheader("🚜 Smart Farming Ecosystem")

c1, c2, c3 = st.columns(3)

with c1:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2909/2909763.png",
        width=180
    )
    st.markdown("### 👨‍🌾 Farmer")

with c2:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/1995/1995470.png",
        width=180
    )
    st.markdown("### 🚜 Tractor")

with c3:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
        width=180
    )
    st.markdown("### 🌾 Crops")

# DATASET

df = pd.read_csv("./data/crop_requirements_starter_dataset.csv")

# INPUTS

st.subheader("📋 Available Crops")

st.dataframe(
    df[["Crop"]],
    use_container_width=True,
    height=250
)

st.subheader("🌾 Agriculture Inputs")

col1, col2 = st.columns(2)

with col1:
    crop = st.text_input(
        "Enter Crop Name"
    )

with col2:
    city = st.text_input(
        "Enter City Name"
    )


# ENVIRONMENT DASHBOARD


st.subheader("🌦 Environmental Indicators")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class='metric-card'>
    <h1>🌡️</h1>
    <h3>Temperature</h3>
    <h2>-- °C</h2>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class='metric-card'>
    <h1>🌧️</h1>
    <h3>Rainfall</h3>
    <h2>-- mm</h2>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class='metric-card'>
    <h1>💨</h1>
    <h3>Wind Speed</h3>
    <h2>-- km/h</h2>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class='metric-card'>
    <h1>🧪</h1>
    <h3>pH</h3>
    <h2>-- </h2>
    </div>
    """, unsafe_allow_html=True)


# SUBMIT BUTTON


button = st.button(
    "🚀 Analyze Agriculture Conditions"
)

# PROCESSING

if button:

    if not city and not crop:
        st.warning(
            "Please enter both City Name and Crop Name."
        )

    elif not city:
        st.warning(
            "Please enter a City Name."
        )

    elif not crop:
        st.warning(
            "Please enter a Crop Name."
        )

    else:

        with st.spinner(
            "🔍 Analyzing Agriculture Conditions..."
        ):

            st.subheader("📍 Location Analysis")

            result_location = run_location_agent(
                city,
                selected_model,
                API_KEY
            )

            st.markdown(
                f"<div class='result-box'>{result_location}</div>",
                unsafe_allow_html=True
            )

            #lat, long = get_coordinates()
            lat=st.session_state.get("latitude")
            long=st.session_state.get("longitude")

            st.subheader("🌦 Weather Analysis")

            weather_result = run_weather_agent(
                lat,
                long,
                selected_model,
                API_KEY
            )

            st.markdown(
                f"<div class='result-box'>{weather_result}</div>",
                unsafe_allow_html=True
            )

            st.subheader("🌱 Soil Analysis")

            soil_result = run_soil_agent(
                lat,
                long,
                selected_model,
                API_KEY
            )

            st.markdown(
                f"<div class='result-box'>{soil_result}</div>",
                unsafe_allow_html=True
            )

            st.subheader("🚜 Agriculture Recommendation")

            agri_result = run_agriculture_agent(
                crop,
                weather_result,
                soil_result,
                selected_model,
                API_KEY
            )

            st.markdown(
                f"<div class='result-box'>{agri_result}</div>",
                unsafe_allow_html=True
            )

# FOOTER

st.markdown("---")

st.markdown(
"""
<center>
<h4 style='color:white;'>
🌱 AI Agro Advisor | Smart Farming with Generative AI 🚜
</h4>
</center>
""",
unsafe_allow_html=True
)